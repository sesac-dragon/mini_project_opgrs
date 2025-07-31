import streamlit as st 
import pandas as pd
import requests
import base64 # base64 인코딩 및 디코딩 처리용
from Crypto.Cipher import AES # AES 암호화 알고리즘 사용
from Crypto.Util.Padding import unpad # AES 복호화 시 패딩 제거
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# 복호화 및 가격 변환 함수


## 복호화함수
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad





def decrypt(encrypted_text, secret):
    """
    AES ECB 모드로 암호화된 텍스트를 복호화합니다.
    
    Args:
        encrypted_text (str): Base64로 인코딩된 암호화된 텍스트
    
    Returns:
        str: 복호화된 평문 텍스트
    """
    # Base64 디코딩
    encrypted_bytes = base64.b64decode(encrypted_text)
    
    # 키 생성
    key = get_key(secret)
    
    # AES 복호화 객체 생성 (ECB 모드)
    cipher = AES.new(key, AES.MODE_ECB)
    
    # 복호화
    decrypted_bytes = cipher.decrypt(encrypted_bytes)
    
    # PKCS7 패딩 제거
    unpadded_bytes = unpad(decrypted_bytes, AES.block_size)
    
    # UTF-8 문자열로 변환
    return unpadded_bytes.decode('utf-8')

def get_key(secret):
    """
    비밀 문자열을 AES 키로 변환합니다.
    키 길이에 따라 적절한 크기로 조정합니다.
    
    Args:
        secret (str): 비밀 문자열
    
    Returns:
        bytes: AES 키 (16, 24, 또는 32 바이트)
    """
    # 문자열을 UTF-8 바이트로 변환
    key_bytes = secret.encode('utf-8')
    length = len(key_bytes)
    
    # 키 길이에 따라 조정
    if length < 16:
        # 16바이트보다 작으면 16바이트로 패딩
        adjusted_key = key_bytes[:16].ljust(16, b'\x00')
    elif length > 16 and length < 24:
        # 16바이트보다 크고 24바이트보다 작으면 24바이트로 조정
        adjusted_key = key_bytes[:24].ljust(24, b'\x00')
    elif length > 24 and length < 32:
        # 24바이트보다 크고 32바이트보다 작으면 32바이트로 조정
        adjusted_key = key_bytes[:32].ljust(32, b'\x00')
    elif length >= 32:
        # 32바이트 이상이면 32바이트로 잘라내기
        adjusted_key = key_bytes[:32]
    else:
        # 정확히 16바이트면 그대로 사용
        adjusted_key = key_bytes
    
    return adjusted_key



# 숫자를 억단위로 변환
def parse_korean_price(text):
    """
    예: '12억 5,000' → 12.5, '9억' → 9.0, '3억8000' → 3.8
    """
    if not isinstance(text, str) or text.strip() == "": 
        return None

    text = text.replace(",", "").replace(" ", "") # 쉼표 및 공백 제거
    eok = 0
    man = 0
    
    # "억"이 포함된 경우 억과 만 단위 분리
    if "억" in text:
        parts = text.split("억")
        eok = int(parts[0]) if parts[0].isdigit() else 0
        if len(parts) > 1 and parts[1].isdigit():
            man = int(parts[1])
    elif text.isdigit(): # "억"이 없고 숫자일 경우
        man = int(text)

    return round(eok + man / 10000, 3)



# 아파트별 API 요청용 정보 딕셔너리 (seq: 아파트 고유 식별자, key: 복호화 키)
apt_info = {
    "마곡엠벨리14단지":{"seq":20288954,"key":'75436879251857920288954'},
    "마곡엠벨리12단지":{"seq":20342347,"key":'75736879054303820342347'},
    "마곡엠벨리15단지":{"seq":20288938,"key":'75836879251917120288938'},
    "마곡엠벨리9단지":{"seq":1500070603,"key":'7533140405975661500070603'},
    "마곡힐스테이트":{"seq":20330992,"key":'75236879096317320330992'}
}


# 개별 아파트 실거래가 데이터를 가져오는 함수
def fetch_apt_data(seq,apt_name,key):
    url = (f"https://asil.kr/app/data/apt_price_m2_newver_6.jsp?sido=11&dealmode=1&building=apt&seq={seq}&m2=0&py=&py_type=&isPyQuery=false&year=9999&u=0&start=0&count=1000&dong_name=&order=")
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://asil.kr/",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    new_data = response.json()

    rows = []
    if new_data and "val" in new_data[0]:
        for monthly in new_data[0]["val"]:
            yyyymm = monthly["yyyymm"]
            for daily in monthly["val"]:
                day = daily["day"]
                for deal in daily["val"]:
                    rows.append({
                        "거래일": f"{yyyymm[:4]}.{yyyymm[4:]}.{day:02}",
                        "칸수": deal.get("floor"),
                        "가격": deal.get("money"),
                        "전원세": deal.get("rent")
                    })
    df = pd.DataFrame(rows)
    
    df['가격'] = df['가격'].apply(lambda x: decrypt(x, key))
    df['전원세'] = df['전원세'].apply(lambda x: decrypt(x, key))
    df['가격(억단위)'] = df['가격'].apply(parse_korean_price)
    df["연도"] = df["거래일"].apply(lambda x: int(x.split(".")[0]))
    df["아파트명"] = apt_name
    return df.groupby("연도")["가격(억단위)"].mean().reset_index(name="평균_가격(억단위)")

select_apt = st.selectbox("아파트를 선택하세요", list(apt_info.keys()))
seq = apt_info[select_apt]["seq"]
key = apt_info[select_apt]["key"]
apt_df = fetch_apt_data(seq, select_apt, key)



# -------------------------
# Streamlit 실행

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Malgun Gothic'  # 한글 폰트 설정
plt.rcParams['axes.unicode_minus'] = False     # 음수 기호 깨짐 방지

st.title(f"마곡역 유동인구 & {select_apt}시세")

# 유동인구 CSV 파일 불러오기

data = pd.read_csv('C:\\Users\\opgrs\\OneDrive\\Desktop\\mini_project\\dashboard\\data\\서울시 지하철 호선별 역별 시간대별 승하차 인원 정보2.csv')

# 유동인구 합산
person_columns = [col for col in data.columns if '승차인원' in col or '하차인원' in col]
data["유동인구"] = data[person_columns].sum(axis=1)
data["연도"] = data["사용월"].astype(str).str[:4].astype(int)

# 마곡역만 필터링
sungsu_df = data[data["지하철역"] == "마곡"]
pop_df = sungsu_df.groupby("연도")["유동인구"].sum().reset_index()

# 2025년도는 1~6월 자료만 있으므로 단순히 2배로 추정
if 2025 in pop_df["연도"].values:
    pop_df.loc[pop_df["연도"] == 2025, "유동인구"] *= 2



# 연도 기준으로 두 데이터 병합
merged = pd.merge(apt_df, pop_df, on="연도")
# 유동인구를 천 명 단위로 환산 (시각화용)
merged["유동인구(천명)"] = (merged["유동인구"] / 1000).round(1)
fig, ax1 = plt.subplots()

# 아파트 시세 (억 단위)
ax1.set_xlabel("연도")
ax1.set_ylabel(f"{select_apt} 시세 (억)", color="blue")
ax1.plot(merged["연도"], merged["평균_가격(억단위)"], color="blue", marker="o")
ax1.tick_params(axis='y', labelcolor="blue")

# 유동인구 (천 명 단위)
ax2 = ax1.twinx()
ax2.set_ylabel("마곡역 유동인구 (천명)", color="red")
ax2.plot(merged["연도"], merged["유동인구(천명)"], color="red", linestyle="--", marker="s")
ax2.tick_params(axis='y', labelcolor="red")

plt.title(f"마곡역 유동인구 {select_apt} 시세")
plt.grid(True)
st.pyplot(fig)





# 모든 아파트 데이터 통합
all_apt = []

for apt_name, info in apt_info.items():
    seq = info["seq"]
    key = info["key"]
    
    
    url_1 = f"https://asil.kr/app/data/apt_price_m2_newver_6.jsp?sido=11&dealmode=1&building=apt&seq={seq}&m2=0&py=&py_type=&isPyQuery=false&year=9999&u=0&start=0&count=1000&dong_name=&order="
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://asil.kr/",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json"
    }
    response = requests.get(url_1, headers=headers)
    new_data = response.json()

    rows = []
    if new_data and "val" in new_data[0]:
        for monthly in new_data[0]["val"]:
            yyyymm = monthly["yyyymm"]
            for daily in monthly["val"]:
                day = daily["day"]
                for deal in daily["val"]:
                    rows.append({
                        "거래일": f"{yyyymm[:4]}.{yyyymm[4:]}.{day:02}",
                        "칸수": deal.get("floor"),
                        "가격": deal.get("money"),
                        "전원세": deal.get("rent"),
                        "아파트명": apt_name
                    })

    df = pd.DataFrame(rows)
    df['가격'] = df['가격'].apply(lambda x: decrypt(x, key))
    df['전원세'] = df['전원세'].apply(lambda x: decrypt(x, key))
    df['가격(억단위)'] = df['가격'].apply(parse_korean_price)
    df['연도'] = df['거래일'].apply(lambda x: int(x.split('.')[0]))
    df['월'] = df['거래일'].apply(lambda x: int(x.split('.')[1]))
    all_apt.append(df)

# 하나의 통합 DataFrame 생성
total_df = pd.concat(all_apt, ignore_index=True)

# 월별 기초통계
st.write("마곡역 아파트들의 월별 기초통계 분석")
monthly_apt = total_df.groupby("월")["가격(억단위)"].agg(["count", "mean", "std", "min", "max"]).reset_index()
st.dataframe(monthly_apt)


# 마곡역 아파트 boxplot
fig, ax = plt.subplots()
st.set_page_config(layout="wide")
plt.title("마곡역 아파트들 Box Plot")
sns.boxplot(data=total_df,x = "월",y="가격(억단위)")
plt.xlabel("월")
plt.ylabel("가격(억단위)")
st.pyplot(plt)






# 데이터들 정규성 검정
import scipy.stats as stats # 통계 분석 라이브러리
import matplotlib.pyplot as plt
import streamlit as st

st.title("마곡역 아파트 가격 정규성 분석 (월별)")

# 월 선택
selected_month = st.selectbox("월을 선택하세요", sorted(total_df["월"].dropna().unique()))

# 해당 월 데이터 필터링
sample = total_df[total_df["월"] == selected_month]["가격(억단위)"].dropna()


# Q-Q plot(데이터가 정규분포를 따르는지 시각적으로 확인하는 그래프) 시각화
fig, ax = plt.subplots()
stats.probplot(sample, dist="norm", plot=ax)
ax.set_title(f"{selected_month}월 Q-Q Plot")
st.pyplot(fig)

# Shapiro-Wilk 정규성 검정 실행
stat, p_value = stats.shapiro(sample)

# 수치 출력
st.subheader("Shapiro-Wilk 정규성 검정 결과")
st.write(f"- 검정 통계량 W: {stat:.4f}")
st.write(f"- p-value: {p_value:.9f}")

# p-value 해석 (유의수준 0.05 기준)
if p_value > 0.05:
    st.success(f"p-value가 0.05보다 크므로, {selected_month}월의 아파트 가격은 정규분포를 따른다고 볼 수 있습니다.")
else:
    st.error(f"p-value가 0.05보다 작으므로, {selected_month}월의 아파트 가격은 정규분포를 따른다고 보기 어렵습니다.")






# 월 단위로 집계된 아파트 평균 시세와 유동인구 합산 데이터

import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# 마곡역 데이터 (연도+월별 집계 + 2025 보정)
magok_df = data[data["지하철역"] == "마곡"].copy()
magok_df["월"] = data["사용월"].astype(str).str[4:].astype(int)
magok_df["연도"] = data["사용월"].astype(str).str[:4].astype(int)

# 연도-월 단위 집계
pop_ym = magok_df.groupby(["연도", "월"])["유동인구"].sum().reset_index()

# 2025년 보정 (1~6월만 존재하기에 2배)
pop_ym.loc[pop_ym["연도"] == 2025, "유동인구"] *= 2
pop_ym["유동인구(천명)"] = (pop_ym["유동인구"] / 1000).round(1)


# 아파트 데이터 
price_ym = total_df[["연도", "월", "가격(억단위)"]].dropna()

# 병합
merged_df = pd.merge(price_ym, pop_ym[["연도", "월", "유동인구(천명)"]], on=["연도", "월"], how="inner")

# Spearman 상관관계 분석(데이터가 정규분포하지 않기 때문에)
rho, p = stats.spearmanr(merged_df["가격(억단위)"], merged_df["유동인구(천명)"])

# 결과
st.title("연-월별 마곡역 아파트 시세 & 유동인구 Spearman 상관분석")
st.write(f"데이터 수: {len(merged_df)}건")

st.subheader("상관분석 결과")
st.write(f"- Spearman's correlation : {rho:.4f}")
st.write(f"- p-value: {p:.4f}")

if p <= 0.05:
    st.success(" 유의미한 상관관계가 있습니다 (p ≤ 0.05)")
else:
    st.info(" 통계적으로 유의미한 상관관계는 없습니다 (p > 0.05)")

# 산점도 시각화
fig, ax = plt.subplots()
sns.scatterplot(data=merged_df, x="유동인구(천명)", y="가격(억단위)", ax=ax)
ax.set_title("성수역 유동인구(천명) vs 아파트 시세(억단위)")
st.pyplot(fig)




st.markdown("## 분석 요약: 마곡역 유동인구 vs 아파트 시세 (Spearman 상관분석)")

st.markdown(f"""
 - Spearman's 상관계수 : {rho:.4f} 
 - p-value : {p:.9f}

--- 
 **상관계수 해석 기준표**

| p 범위      | 해석              |
|------------|-------------------|
| 0.00-0.19  | 매우 약한 상관     |
| 0.20-0.39  | 약한 상관         |
| 0.40-0.59  | 중간 정도의 상관 |
| 0.60-0.79  | 강한 상관         |
| 0.80-1.00  | 매우 강한 상관     |

**해석 요약:**

- 상관계수  = {rho:.4f}는 강한 정도의 양의 상관관계를 의미합니다
- p-value = {p:.4f}로, 일반적인 유의수준 0.05보다 작아 통계적으로 유의미한 상관관계가 있다고 볼 수 있습니다
- 즉, 마곡역 유동인구가 많을수록 아파트 시세가 높아지는 경향이 관찰되었습니다

---

 주의사항:

- 본 분석은 **상관관계(correlation)**를 확인하는 것이며, **인과관계(causation)**를 증명하는 것은 아닙니다
- 아파트 시세에는 유동인구 외에도 입지, 학군, 브랜드, 금리 등 다양한 요인이 영향을 미칠 수 있습니다
""")

st.subheader("데이터 자료형 확인")
st.write(merged_df[["가격(억단위)", "유동인구(천명)"]].dtypes)
