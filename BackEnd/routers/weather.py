from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import kma_service, airkorea_service
from schemas.weather import HourlyForecastCreate, HourlyForecastResponse, DustCreate, DustResponse, WeeklyForecastCreate, WeeklyForecastResponse, UVCreate, UVResponse
import crud
from typing import List

router = APIRouter(
    prefix="/api/weather",
    tags=["weather"],
    responses={404: {"description": "Not found"}},
)

# --- Current Weather (Real-time, No DB) ---

@router.get("/current", response_model=dict)
async def get_current_weather_realtime(nx: int = 60, ny: int = 127):
    """
    Fetches current weather (Ultra Short-term Nowcast) directly from KMA API.
    Does NOT save to database.
    """
    try:
        data = await kma_service.fetch_ultra_srt_ncst(nx, ny)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Daily Forecast (Short-term, Save to DB) ---

@router.post("/daily", response_model=List[HourlyForecastResponse])
async def log_daily_forecast(nx: int = 60, ny: int = 127, db: Session = Depends(get_db)):
    """
    Fetches 24-hour forecast (Short-term VilageFcst) and saves to database.
    Should be called hourly.
    """
    try:
        data_list = await kma_service.fetch_vilage_fcst(nx, ny)
        saved_items = []
        for item in data_list:
            weather_create = HourlyForecastCreate(**item)
            db_weather = crud.create_hourly_forecast(db, weather_create)
            saved_items.append(db_weather)
        return saved_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/daily", response_model=List[HourlyForecastResponse])
def get_saved_daily_forecast(nx: int = 60, ny: int = 127, db: Session = Depends(get_db)):
    """
    Returns the next 24 hours of forecast data stored in the database.
    """
    db_weather = crud.get_hourly_forecasts(db, nx, ny, limit=24)
    if not db_weather:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return db_weather

# --- Weekly Forecast (Short+Mid, Save to DB) ---

@router.post("/weekly", response_model=WeeklyForecastResponse)
async def log_weekly_forecast(nx: int = 60, ny: int = 127, regId_temp: str = "11B10101", regId_land: str = "11B00000", db: Session = Depends(get_db)):
    """
    Fetches Weekly Forecast (Day 1-3: Short-term, Day 4-7: Mid-term) and saves to database.
    Should be called daily.
    """
    try:
        data = await kma_service.fetch_weekly_weather(nx, ny, regId_temp, regId_land)
        weekly_create = WeeklyForecastCreate(**data)
        db_weekly = crud.create_weekly_forecast(db, weekly_create)
        return db_weekly
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weekly", response_model=WeeklyForecastResponse)
def get_saved_weekly_forecast(regId: str = "11B00000", db: Session = Depends(get_db)):
    """
    Returns the latest weekly weather data stored in the database.
    """
    db_weekly = crud.get_latest_weekly_forecast(db, regId)
    if db_weekly is None:
        raise HTTPException(status_code=404, detail="Weekly weather data not found")
    return db_weekly

# --- Dust & UV (Existing) ---

@router.post("/log/dust", response_model=DustResponse)
async def log_dust_info(station_name: str = "종로구", db: Session = Depends(get_db)):
    """
    Fetches dust info from AirKorea API and saves it to the database.
    """
    try:
        data = await airkorea_service.fetch_dust_info(station_name)
        dust_create = DustCreate(**data)
        db_dust = crud.create_dust(db, dust_create)
        return db_dust
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dust", response_model=DustResponse)
def get_dust_info(station_name: str = "종로구", db: Session = Depends(get_db)):
    """
    Returns the latest dust data stored in the database.
    """
    db_dust = crud.get_latest_dust(db, station_name)
    if db_dust is None:
        raise HTTPException(status_code=404, detail="Dust data not found")
    return db_dust

@router.post("/log/uv", response_model=UVResponse)
async def log_uv_info(areaNo: str = "1100000000", db: Session = Depends(get_db)):
    """
    Fetches UV info from KMA API and saves it to the database.
    Default: Seoul (1100000000)
    """
    try:
        data = await kma_service.fetch_uv_index(areaNo)
        uv_create = UVCreate(**data)
        db_uv = crud.create_uv(db, uv_create)
        return db_uv
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/uv", response_model=UVResponse)
def get_uv_info(areaNo: str = "1100000000", db: Session = Depends(get_db)):
    """
    Returns the latest UV data stored in the database.
    """
    db_uv = crud.get_latest_uv(db, areaNo)
    if db_uv is None:
        raise HTTPException(status_code=404, detail="UV data not found")
    return db_uv
