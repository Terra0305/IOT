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
    regId: str
    fcstDate: str
    rnStAm: Optional[int] = None
    rnStPm: Optional[int] = None
    wfAm: Optional[str] = None
    wfPm: Optional[str] = None
    taMin: Optional[int] = None
    taMax: Optional[int] = None

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
