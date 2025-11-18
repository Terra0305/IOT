#날씨모델
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from database import Base

class Weather(Base):
  """날씨 모델"""
  __tablename__ = 'weather'

  # 1. 복합 기본키 (Composite Primary Key) 설정
  # SQLAlchemy에서는 primary_key=True를 여러 컬럼에 지정하면 자동으로 복합키가 됩니다.
  base_date = Column(String(8), primary_key=True, nullable=False, comment="기준 날짜 (YYYYMMDD)")
  base_time = Column(String(4), primary_key=True, nullable=False, comment="기준 시간 (HHMM)")
  nx = Column(Integer, primary_key=True, nullable=False, comment="예보지점 X 좌표")
  ny = Column(Integer, primary_key=True, nullable=False, comment="예보지점 Y 좌표")
  # 2. 관측 데이터 컬럼 (API 코드 매핑)
  # T1H: 기온 (소수점 포함 가능하므로 Float)
  temperature = Column(Float, comment="기온 (℃)")
  
  # REH: 습도 (보통 정수지만, 계산 등을 위해 Float 허용 추천)
  humidity = Column(Float, comment="습도 (%)")
  
  # RN1: 1시간 강수량 (실수형)
  rain_1h = Column(Float, comment="1시간 강수량 (mm)")
    
  # PTY: 강수형태 (코드값: 0,1,2... 정수)
  precip_type = Column(Integer, comment="강수형태 (코드)")
    
  # WSD: 풍속
  wind_speed = Column(Float, comment="풍속 (m/s)")
    
  # VEC: 풍향
  wind_direction = Column(Float, comment="풍향 (deg)")
    
  # UUU: 동서바람성분
  wind_ew = Column(Float, comment="동서바람성분 (m/s)")
    
  # VVV: 남북바람성분
  wind_ns = Column(Float, comment="남북바람성분 (m/s)")

  def __repr__(self):
    return f"<Weather {self.base_date} {self.base_time} ({self.nx}, {self.ny}) Temp:{self.temperature}>"