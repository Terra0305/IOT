# 날씨 및 환경 정보 모델 정의
from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from database import Base

class HourlyForecast(Base):
    """
    기상청 단기예보 (Hourly Forecast)
    - 24시간 상세 예보
    """
    __tablename__ = 'hourly_forecast'

    # 복합 기본키: 날짜 + 시간 + 좌표
    base_date = Column(String(8), primary_key=True, nullable=False, comment="기준 날짜 (YYYYMMDD)")
    base_time = Column(String(4), primary_key=True, nullable=False, comment="기준 시간 (HHMM)")
    nx = Column(Integer, primary_key=True, nullable=False, comment="예보지점 X 좌표")
    ny = Column(Integer, primary_key=True, nullable=False, comment="예보지점 Y 좌표")

    # 관측 데이터
    temperature = Column(Float, comment="기온 (T1H) ℃")
    humidity = Column(Float, comment="습도 (REH) %")
    rain_1h = Column(Float, comment="1시간 강수량 (RN1) mm")
    precip_type = Column(Integer, comment="강수형태 (PTY) 코드")
    wind_speed = Column(Float, comment="풍속 (WSD) m/s")
    wind_direction = Column(Float, comment="풍향 (VEC) deg")
    wind_ew = Column(Float, comment="동서바람성분 (UUU) m/s")
    wind_ns = Column(Float, comment="남북바람성분 (VVV) m/s")

    def __repr__(self):
        return f"<Hourly {self.base_date} {self.base_time} ({self.nx}, {self.ny})>"

class WeeklyForecast(Base):
    """
    기상청 중기예보 (Weekly Forecast)
    - 주간 기온 및 육상 예보
    """
    __tablename__ = 'weekly_forecast'

    # 복합 기본키: 발표 시각 + 지역 코드
    tmFc = Column(String(14), primary_key=True, nullable=False, comment="발표시각 (YYYYMMDDHHMM)")
    regId = Column(String(10), primary_key=True, nullable=False, comment="예보구역코드")

    # 예보 데이터 (1일 후 ~ 7일 후)
    # 1일 후
    rnSt1Am = Column(Integer, comment="1일 후 오전 강수확률")
    rnSt1Pm = Column(Integer, comment="1일 후 오후 강수확률")
    wf1Am = Column(String(20), comment="1일 후 오전 날씨")
    wf1Pm = Column(String(20), comment="1일 후 오후 날씨")
    taMin1 = Column(Integer, comment="1일 후 최저기온")
    taMax1 = Column(Integer, comment="1일 후 최고기온")

    # 2일 후
    rnSt2Am = Column(Integer, comment="2일 후 오전 강수확률")
    rnSt2Pm = Column(Integer, comment="2일 후 오후 강수확률")
    wf2Am = Column(String(20), comment="2일 후 오전 날씨")
    wf2Pm = Column(String(20), comment="2일 후 오후 날씨")
    taMin2 = Column(Integer, comment="2일 후 최저기온")
    taMax2 = Column(Integer, comment="2일 후 최고기온")

    # 3일 후
    rnSt3Am = Column(Integer, comment="3일 후 오전 강수확률")
    rnSt3Pm = Column(Integer, comment="3일 후 오후 강수확률")
    wf3Am = Column(String(20), comment="3일 후 오전 날씨")
    wf3Pm = Column(String(20), comment="3일 후 오후 날씨")
    taMin3 = Column(Integer, comment="3일 후 최저기온")
    taMax3 = Column(Integer, comment="3일 후 최고기온")

    # 4일 후
    rnSt4Am = Column(Integer, comment="4일 후 오전 강수확률")
    rnSt4Pm = Column(Integer, comment="4일 후 오후 강수확률")
    wf4Am = Column(String(20), comment="4일 후 오전 날씨")
    wf4Pm = Column(String(20), comment="4일 후 오후 날씨")
    taMin4 = Column(Integer, comment="4일 후 최저기온")
    taMax4 = Column(Integer, comment="4일 후 최고기온")

    # 5일 후
    rnSt5Am = Column(Integer, comment="5일 후 오전 강수확률")
    rnSt5Pm = Column(Integer, comment="5일 후 오후 강수확률")
    wf5Am = Column(String(20), comment="5일 후 오전 날씨")
    wf5Pm = Column(String(20), comment="5일 후 오후 날씨")
    taMin5 = Column(Integer, comment="5일 후 최저기온")
    taMax5 = Column(Integer, comment="5일 후 최고기온")

    # 6일 후
    rnSt6Am = Column(Integer, comment="6일 후 오전 강수확률")
    rnSt6Pm = Column(Integer, comment="6일 후 오후 강수확률")
    wf6Am = Column(String(20), comment="6일 후 오전 날씨")
    wf6Pm = Column(String(20), comment="6일 후 오후 날씨")
    taMin6 = Column(Integer, comment="6일 후 최저기온")
    taMax6 = Column(Integer, comment="6일 후 최고기온")

    # 7일 후
    rnSt7Am = Column(Integer, comment="7일 후 오전 강수확률")
    rnSt7Pm = Column(Integer, comment="7일 후 오후 강수확률")
    wf7Am = Column(String(20), comment="7일 후 오전 날씨")
    wf7Pm = Column(String(20), comment="7일 후 오후 날씨")
    taMin7 = Column(Integer, comment="7일 후 최저기온")
    taMax7 = Column(Integer, comment="7일 후 최고기온")

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