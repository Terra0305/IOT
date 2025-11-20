from pydantic import BaseModel
from typing import Optional, List

# --- Common ---
class MessageResponse(BaseModel):
    message: str

# --- Weather (Hourly) ---
class HourlyForecastBase(BaseModel):
    base_date: str
    base_time: str
    nx: int
    ny: int
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    rain_1h: Optional[float] = None
    precip_type: Optional[int] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None
    wind_ew: Optional[float] = None
    wind_ns: Optional[float] = None

class HourlyForecastCreate(HourlyForecastBase):
    pass

class HourlyForecastResponse(HourlyForecastBase):
    class Config:
        from_attributes = True

# --- Weather (Weekly) ---
class WeeklyForecastBase(BaseModel):
    tmFc: str
    regId: str
    # 1일 후
    rnSt1Am: Optional[int] = None
    rnSt1Pm: Optional[int] = None
    wf1Am: Optional[str] = None
    wf1Pm: Optional[str] = None
    taMin1: Optional[int] = None
    taMax1: Optional[int] = None

    # 2일 후
    rnSt2Am: Optional[int] = None
    rnSt2Pm: Optional[int] = None
    wf2Am: Optional[str] = None
    wf2Pm: Optional[str] = None
    taMin2: Optional[int] = None
    taMax2: Optional[int] = None

    # 3일 후
    rnSt3Am: Optional[int] = None
    rnSt3Pm: Optional[int] = None
    wf3Am: Optional[str] = None
    wf3Pm: Optional[str] = None
    taMin3: Optional[int] = None
    taMax3: Optional[int] = None

    # 4일 후
    rnSt4Am: Optional[int] = None
    rnSt4Pm: Optional[int] = None
    wf4Am: Optional[str] = None
    wf4Pm: Optional[str] = None
    taMin4: Optional[int] = None
    taMax4: Optional[int] = None

    # 5일 후
    rnSt5Am: Optional[int] = None
    rnSt5Pm: Optional[int] = None
    wf5Am: Optional[str] = None
    wf5Pm: Optional[str] = None
    taMin5: Optional[int] = None
    taMax5: Optional[int] = None

    # 6일 후
    rnSt6Am: Optional[int] = None
    rnSt6Pm: Optional[int] = None
    wf6Am: Optional[str] = None
    wf6Pm: Optional[str] = None
    taMin6: Optional[int] = None
    taMax6: Optional[int] = None

    # 7일 후
    rnSt7Am: Optional[int] = None
    rnSt7Pm: Optional[int] = None
    wf7Am: Optional[str] = None
    wf7Pm: Optional[str] = None
    taMin7: Optional[int] = None
    taMax7: Optional[int] = None

class WeeklyForecastCreate(WeeklyForecastBase):
    pass

class WeeklyForecastResponse(WeeklyForecastBase):
    class Config:
        from_attributes = True

# --- Dust ---
class DustBase(BaseModel):
    dataTime: str
    stationName: str
    pm10Value: Optional[str] = None
    pm10Grade: Optional[str] = None
    pm25Value: Optional[str] = None
    pm25Grade: Optional[str] = None
    khaiValue: Optional[str] = None
    khaiGrade: Optional[str] = None

class DustCreate(DustBase):
    pass

class DustResponse(DustBase):
    class Config:
        from_attributes = True

# --- UV ---
class UVBase(BaseModel):
    date: str
    areaNo: str
    today: Optional[str] = None
    tomorrow: Optional[str] = None

class UVCreate(UVBase):
    pass

class UVResponse(UVBase):
    class Config:
        from_attributes = True
