LOAD DATA LOCAL INFILE "C:\\Users\\opgrs\\OneDrive\\Desktop\\미니 프로젝트\\11개 한강공원 쓰레기 처리현황(2022~2023).csv"
INTO TABLE Park
CHARACTER SET utf8
FIELDS TERMINATED BY `,`
LINES TERMINATED BY `\n`
IGNORE 1 LINES; 

INTO TABLE Park
CHARACTER SET utf8
FIELDS TERMINATED BY `,`
LINES TERMINATED BY `\n`
IGNORE 1 LINES; 



CREATE TABLE Park(
    Date_ Datetime NOT NULL,
    광나루 int,
    잠실  int,
    잠원 int,
    반포 int,
    여의도 int,
    양화 int,
    강서 int,
    뚝섬 int,
    이촌 int,
    난지 int,
    망원 int,
    기타 int

    
);

SELECT SUM(*)
FROM Park;

CREATE TABLE Date(
    Year_ int,
    Month_  int,
    Date_ int,
    Day_ varchar(255) 
);

CREATE TABLE Time_Table(
    아침 int,
    낮 int,
    저녁 int 
);

CREATE TABLE User_Table(
    아침 int,
    낮 int,
    저녁 int 
);


LOAD DATA LOCAL INFILE `C:\\Users\\opgrs\\OneDrive\\Desktop\\미니 프로젝트\\11개 한강공원 쓰레기 처리현황(2022~2023).csv`
INTO TABLE park
FIELDS TERMINATED BY `,` 
LINES TERMINATED BY `\n`
IGNORE 1 ROWS;

RENAME TABLE Park TO P_Trash_22_23;


CREATE TABLE Park(
    Park_Name varchar(255),
    PRIMARY KEY(Park_Name) 
);

INSERT INTO Park(Park_Name)
VALUES(`광나루`),(`잠실`),(`잠원`),(`여의도`),(`양화`),(`강서`),(`뚝섬`),(`이촌`),(`난지`),(`망원`),(`기타`)

CREATE TABLE Park_Trash_22_23(
    Park VARCHAR(255) PRIMARY KEY,
    Date_ Datetime,
    Trash_22_23 int,
    FOREIGN KEY (Park) REFERENCES Park(Park_Name) 
);



LOAD DATA LOCAL INFILE `C:\\Users\\opgrs\\OneDrive\\Desktop\\미니 프로젝트\\11개 한강공원 쓰레기 처리현황(2022~2023).csv`
INTO TABLE Park_Trash_22_23
FIELDS TERMINATED BY `,` 
LINES TERMINATED BY `\n`
IGNORE 1 ROWS;


INSERT INTO Park_Trash_22_23(Date_) VALUES
(`2022-01-31`),
(`2022-02-28`),
(`2022-03-31`),
(`2022-04-30`),
(`2022-05-31`),
(`2022-06-30`),
(`2022-07-31`),
(`2022-08-31`),
(`2022-09-30`),
(`2022-10-31`),
(`2022-11-30`),
(`2022-12-31`),
(`2023-01-31`),
(`2023-02-28`),
(`2023-03-31`),
(`2023-04-30`),
(`2023-05-31`),
(`2023-06-30`),
(`2023-07-31`),
(`2023-08-31`),
(`2023-09-30`),
(`2023-10-31`),
(`2023-11-30`),
(`2023-12-31`);


INSERT INTO Park_Trash_22_23(Park)
VALUES(`광나루`),(`잠실`),(`잠원`),(`여의도`),(`양화`),(`강서`),(`뚝섬`),(`이촌`),(`난지`),(`망원`),(`기타`)


CREATE TABLE Park_Trash_22_23 (
    Park VARCHAR(255),
    Date_ DATETIME,
    Trash_22_23 INT,
    PRIMARY KEY (Park, Date_),
    FOREIGN KEY (Park) REFERENCES Park(Park_Name)
);


################################################################################################

CREATE TABLE Subway_People(
    Date_ int ,
    호선명 VARCHAR(255),
    지하철역 VARCHAR(255),
    `04-05시 승차인원` INT,
    `04-05시 하차인원` int,
    `05-06시 승차인원` int,
    `05-06시 하차인원` int,
    `06-07시 승차인원` int,
    `06-07시 하차인원` int,
    `07-08시 승차인원` int,
    `07-08시 하차인원` int,
    `08-09시 승차인원` int,
    `08-09시 하차인원` int,
    `09-10시 승차인원` int,
    `09-10시 하차인원` int,
    `10-11시 승차인원` int,
    `10-11시 하차인원` int,
    `11-12시 승차인원` int,
    `11-12시 하차인원` int,
    `12-13시 승차인원` int,
    `12-13시 하차인원` int,
    `13-14시 승차인원` int,
    `13-14시 하차인원` int,
    `14-15시 승차인원` int,
    `14-15시 하차인원` int,
    `15-16시 승차인원` int,
    `15-16시 하차인원` int,
    `16-17시 승차인원` int,
    `16-17시 하차인원` int,
    `17-18시 승차인원` int,
    `17-18시 하차인원` int,
    `18-19시 승차인원` int,
    `18-19시 하차인원` int,
    `19-20시 승차인원` int,
    `19-20시 하차인원` int,
    `20-21시 승차인원` int,
    `20-21시 하차인원` int,
    `21-22시 승차인원` int,
    `21-22시 하차인원` int,
    `22-23시 승차인원` int,
    `22-23시 하차인원` int,
    `23-24시 승차인원` int,
    `23-24시 하차인원` int,
    `00-01시 승차인원` int,
    `00-01시 하차인원` int,
    `01-02시 승차인원` int,
    `01-02시 하차인원` int,
    `02-03시 승차인원` int,
    `02-03시 하차인원` int,
    `03-04시 승차인원` int,
    `03-04시 하차인원` int
  
);

LOAD DATA LOCAL INFILE 'C:\\Users\\opgrs\\OneDrive\\Desktop\\미니 프로젝트\\서울시 지하철 호선별 역별 시간대별 승하차 인원 정보2.csv'
INTO TABLE Subway_People
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


CREATE TABLE Subway_2015 AS
SELECT *
FROM Subway_People
WHERE Date_ LIKE '2015%';

CREATE TABLE Subway_2016 AS
SELECT *
FROM Subway_People
WHERE Date_ LIKE '2016%';

CREATE TABLE Subway_2017 AS
SELECT *
FROM Subway_People
WHERE Date_ LIKE '2017%';

CREATE TABLE Subway_2018 AS
SELECT *
FROM Subway_People
WHERE Date_ LIKE '2018%';

CREATE TABLE Subway_2019 AS
SELECT *
FROM Subway_People
WHERE Date_ LIKE '2019%';

CREATE TABLE Subway_2020 AS
SELECT *
FROM Subway_People
WHERE Date_ LIKE '2020%';

CREATE TABLE Subway_2021 AS
SELECT *
FROM Subway_People
WHERE Date_ LIKE '2021%';

CREATE TABLE Subway_2022 AS
SELECT *
FROM Subway_People
WHERE Date_ LIKE '2022%';

CREATE TABLE Subway_2023 AS
SELECT *
FROM Subway_People
WHERE Date_ LIKE '2023%';

CREATE TABLE Subway_2024 AS
SELECT *
FROM Subway_People
WHERE Date_ LIKE '2024%';

CREATE TABLE Subway_2025 AS
SELECT *
FROM Subway_People
WHERE Date_ LIKE '2025%';