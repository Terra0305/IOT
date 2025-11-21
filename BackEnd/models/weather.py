# 날씨 및 환경 정보 모델 정의
from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from database import Base

class HourlyForecast(Base):
    """
    기상청 단기예보 (Vilage Forecast) - 24시간 예보
    """
    __tablename__ = 'hourly_forecast'

    # 복합 기본키: 예보 날짜 + 예보 시간 + 좌표
    fcstDate = Column(String(8), primary_key=True, nullable=False, comment="예보 날짜 (YYYYMMDD)")
    fcstTime = Column(String(4), primary_key=True, nullable=False, comment="예보 시간 (HHMM)")
    nx = Column(Integer, primary_key=True, nullable=False, comment="예보지점 X 좌표")
    ny = Column(Integer, primary_key=True, nullable=False, comment="예보지점 Y 좌표")

    # 예보 데이터
    temperature = Column(Float, comment="1시간 기온 (TMP) ℃")
    humidity = Column(Integer, comment="습도 (REH) %")
    sky = Column(Integer, comment="하늘상태 (SKY) 1:맑음, 3:구름많음, 4:흐림")
    pty = Column(Integer, comment="강수형태 (PTY) 0:없음, 1:비, 2:비/눈, 3:눈, 4:소나기")
    pop = Column(Integer, comment="강수확률 (POP) %")
    pcp = Column(String(20), comment="1시간 강수량 (PCP)")
    vec = Column(Float, comment="풍향 (VEC) deg")
    wsd = Column(Float, comment="풍속 (WSD) m/s")

    def __repr__(self):
        return f"<Hourly {self.fcstDate} {self.fcstTime} ({self.nx}, {self.ny})>"

class WeeklyForecast(Base):
    """
    기상청 주간예보 (Weekly Forecast)
    - 단기예보(1~3일) + 중기예보(4~7일) 병합
    """
    __tablename__ = 'weekly_forecast'

    # 복합 기본키: 발표 시각 + 구역 코드
    tmFc = Column(String(14), primary_key=True, nullable=False, comment="발표시각 (YYYYMMDDHHMM)")
    regId = Column(String(10), primary_key=True, nullable=False, comment="예보구역코드")

    # 1일 ~ 7일 예보 데이터
    # Day 1
    rnSt1Am = Column(Integer, nullable=True)
    rnSt1Pm = Column(Integer, nullable=True)
    wf1Am = Column(String(20), nullable=True)
    wf1Pm = Column(String(20), nullable=True)
    taMin1 = Column(Integer, nullable=True)
    taMax1 = Column(Integer, nullable=True)
    
    # Day 2
    rnSt2Am = Column(Integer, nullable=True)
    rnSt2Pm = Column(Integer, nullable=True)
    wf2Am = Column(String(20), nullable=True)
    wf2Pm = Column(String(20), nullable=True)
    taMin2 = Column(Integer, nullable=True)
    taMax2 = Column(Integer, nullable=True)

    # Day 3
    rnSt3Am = Column(Integer, nullable=True)
    rnSt3Pm = Column(Integer, nullable=True)
    wf3Am = Column(String(20), nullable=True)
    wf3Pm = Column(String(20), nullable=True)
    taMin3 = Column(Integer, nullable=True)
    taMax3 = Column(Integer, nullable=True)

    # Day 4
    rnSt4Am = Column(Integer, nullable=True)
    rnSt4Pm = Column(Integer, nullable=True)
    wf4Am = Column(String(20), nullable=True)
    wf4Pm = Column(String(20), nullable=True)
    taMin4 = Column(Integer, nullable=True)
    taMax4 = Column(Integer, nullable=True)

    # Day 5
    rnSt5Am = Column(Integer, nullable=True)
    rnSt5Pm = Column(Integer, nullable=True)
    wf5Am = Column(String(20), nullable=True)
    wf5Pm = Column(String(20), nullable=True)
    taMin5 = Column(Integer, nullable=True)
    taMax5 = Column(Integer, nullable=True)

    # Day 6
    rnSt6Am = Column(Integer, nullable=True)
    rnSt6Pm = Column(Integer, nullable=True)
    wf6Am = Column(String(20), nullable=True)
    wf6Pm = Column(String(20), nullable=True)
    taMin6 = Column(Integer, nullable=True)
    taMax6 = Column(Integer, nullable=True)

    # Day 7
    rnSt7Am = Column(Integer, nullable=True)
    rnSt7Pm = Column(Integer, nullable=True)
    wf7Am = Column(String(20), nullable=True)
    wf7Pm = Column(String(20), nullable=True)
    taMin7 = Column(Integer, nullable=True)
    taMax7 = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Weekly {self.tmFc} {self.regId}>"

class Dust(Base):
    """
    에어코리아 대기오염정보 (Fine Dust)
    - 미세먼지 (PM10), 초미세먼지 (PM2.5)
    """
    __tablename__ = 'dust'

    # 복합 기본키: 측정 일시 + 측정소 명
    dataTime = Column(String(20), primary_key=True, nullable=False, comment="측정일시 (YYYY-MM-DD HH:MM)")
    stationName = Column(String(20), primary_key=True, nullable=False, comment="측정소명")

    pm10Value = Column(String(10), comment="미세먼지(PM10) 농도") # 가끔 '-' 같은 문자가 올 수 있어 String 처리 후 변환 권장
    pm10Grade = Column(String(5), comment="미세먼지 등급")
    pm25Value = Column(String(10), comment="초미세먼지(PM2.5) 농도")
    pm25Grade = Column(String(5), comment="초미세먼지 등급")
    khaiValue = Column(String(10), comment="통합대기환경수치")
    khaiGrade = Column(String(5), comment="통합대기환경지수 등급")

    def __repr__(self):
        return f"<Dust {self.dataTime} {self.stationName}>"

class UV(Base):
    """
    기상청 생활기상지수 (UV Index)
    - 자외선 지수
    """
    __tablename__ = 'uv'

    # 복합 기본키: 발표 시각 + 지역 코드
    date = Column(String(14), primary_key=True, nullable=False, comment="발표시각 (YYYYMMDDHH)")
    areaNo = Column(String(10), primary_key=True, nullable=False, comment="지역코드")

    today = Column(String(5), comment="오늘 자외선 지수") # 예측값은 문자열이나 숫자로 올 수 있음
    tomorrow = Column(String(5), comment="내일 자외선 지수")

    def __repr__(self):
        return f"<UV {self.date} {self.areaNo}>"