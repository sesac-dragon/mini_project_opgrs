import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

def main():
    st.title('지하철 유동인구')

    # CSV 불러오기
    data = pd.read_csv('C:\\Users\\opgrs\\OneDrive\\Desktop\\mini_project\\서울시 지하철 호선별 역별 시간대별 승하차 인원 정보2.csv')
    st.dataframe(data)

    st.title("서울시 지하철역 유동인구 변화 분석")

    # 승하차 컬럼 뽑기
    person_columns = []
    for col in data.columns:
        if '승차인원' in col or '하차인원' in col:
            person_columns.append(col)

    # 유동인구 계산
    data["유동인구"] = 0
    for col in person_columns:
        data["유동인구"] += data[col]

    # 연도 계산
    year_list = []
    for y in range(len(data)):
        month = data.loc[y,'사용월']
        year = month // 100
        year_list.append(year)
    data['연도'] = year_list

    # 연도별 역별 유동인구 집계
    info = data.groupby(['연도','지하철역'])['유동인구'].sum().reset_index()

    # 딕셔너리 만들기
    subway_dict = {}
    for i in range(len(info)):
        station = info.loc[i,'지하철역']
        year = info.loc[i,'연도']
        float_pop = info.loc[i,'유동인구']

        if station not in subway_dict:
            subway_dict[station] = {}

        subway_dict[station][year] = float_pop

    
    
    
    # 데이터테이블
    table = pd.DataFrame.from_dict(subway_dict, orient="index")

    if 2015 in table.columns and 2024 in table.columns:

        # 2025 데이터는 6월까지 있어서 2024로 계산
        table["증감폭"] = table[2024] - table[2015]
        table = table.dropna(subset=["증감폭"])

        top_increase = table["증감폭"].sort_values(ascending=False).head(10)
        top_decrease = table["증감폭"].sort_values(ascending=True).head(10)


        # 증가율 계산
        table = table[table[2015]>0]
        table["증가율"] = (table["증감폭"]/table[2015])*100
        top_increase_rate = table["증가율"].sort_values(ascending=False).head(10)

        st.subheader("2015~2024 유동인구 증가율")
        st.bar_chart(top_increase_rate)


        st.subheader("유동인구 증가 Top 10")
        st.bar_chart(top_increase)

        st.subheader("유동인구 감소 Top 10")
        st.bar_chart(top_decrease)

        st.subheader("지하철역 선택하여 연도별 유동인구 보기")
        selected_station = st.selectbox("지하철역을 선택하세요", table.index)

        if selected_station:
            st.line_chart(table.loc[selected_station].drop("증감폭"))

        st.subheader("유동인구 증가 Top 10 그래프")
        select_top_station = st.selectbox("Top 10 지하철 역 중 선택하세요",top_increase.index)

        if select_top_station:
            st.line_chart(table.loc[select_top_station].drop("증감폭"))




# sql로 전체 유동인구 구해서 계산
conn = pymysql.connect(
    host='localhost',
    user = 'opgrs',
    password='test1234',
    db = 'mini_project',
    charset = 'utf8mb4'
)

years_data = list(range(2015,2025))
years_data_in = []

for y in years_data:
    table = f"subway_{y}"

    query = f"""
        SELECT
            SUM(`04-05시 승차인원` + `04-05시 하차인원` +
                   `05-06시 승차인원` + `05-06시 하차인원` +
                   `06-07시 승차인원` + `06-07시 하차인원` +
                   `07-08시 승차인원` + `07-08시 하차인원` +
                   `08-09시 승차인원` + `08-09시 하차인원` +
                   `09-10시 승차인원` + `09-10시 하차인원` +
                   `10-11시 승차인원` + `10-11시 하차인원` +
                   `11-12시 승차인원` + `11-12시 하차인원` +
                   `12-13시 승차인원` + `12-13시 하차인원` +
                   `13-14시 승차인원` + `13-14시 하차인원` +
                   `14-15시 승차인원` + `14-15시 하차인원` +
                   `15-16시 승차인원` + `15-16시 하차인원` +
                   `16-17시 승차인원` + `16-17시 하차인원` +
                   `17-18시 승차인원` + `17-18시 하차인원` +
                   `18-19시 승차인원` + `18-19시 하차인원` +
                   `19-20시 승차인원` + `19-20시 하차인원` +
                   `20-21시 승차인원` + `20-21시 하차인원` +
                   `21-22시 승차인원` + `21-22시 하차인원` +
                   `22-23시 승차인원` + `22-23시 하차인원` +
                   `23-24시 승차인원` + `23-24시 하차인원` +
                   `00-01시 승차인원` + `00-01시 하차인원` +
                   `01-02시 승차인원` + `01-02시 하차인원` +
                   `02-03시 승차인원` + `02-03시 하차인원` +
                   `03-04시 승차인원` + `03-04시 하차인원`)
                   AS 총유동인구
                   FROM subway_{y}
            """
    
    df = pd.read_sql(query, conn)
    total = int(df.loc[0, '총유동인구'])
    years_data_in.append({"연도": y, "총유동인구": total})


conn.close()

year_df = pd.DataFrame(years_data_in)

st.subheader("연도별 유동인구")
st.line_chart(year_df.set_index("연도"))



if __name__ == "__main__":
    main()