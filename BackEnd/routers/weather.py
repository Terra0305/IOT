from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import kma_service, airkorea_service
from schemas.weather import HourlyForecastCreate, HourlyForecastResponse, DustCreate, DustResponse, WeeklyForecastCreate, WeeklyForecastResponse, UVCreate, UVResponse
import crud

router = APIRouter(
    prefix="/api/weather",
    tags=["weather"],
    responses={404: {"description": "Not found"}},
)

# --- Logging APIs (Write to DB) ---

@router.post("/log/current", response_model=HourlyForecastResponse)
async def log_current_weather(nx: int = 60, ny: int = 127, db: Session = Depends(get_db)):
    """
    Fetches current weather (Short-term) from KMA API and saves it to the database.
    """
    try:
        data = await kma_service.fetch_ultra_srt_ncst(nx, ny)
        weather_create = HourlyForecastCreate(**data)
        db_weather = crud.create_hourly_forecast(db, weather_create)
        return db_weather
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/log/weekly", response_model=WeeklyForecastResponse)
async def log_weekly_weather(regId_temp: str = "11B10101", regId_land: str = "11B00000", db: Session = Depends(get_db)):
    """
    Fetches weekly weather (Mid-term) from KMA API and saves it to the database.
    Default: Seoul (11B10101), Seoul/Gyeonggi (11B00000)
    """
    try:
        data = await kma_service.fetch_mid_term_forecast(regId_temp, regId_land)
        weekly_create = WeeklyForecastCreate(**data)
        db_weekly = crud.create_weekly_forecast(db, weekly_create)
        return db_weekly
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

# --- Reading APIs (Read from DB) ---

@router.get("/current", response_model=HourlyForecastResponse)
def get_current_weather(nx: int = 60, ny: int = 127, db: Session = Depends(get_db)):
    """
    Returns the latest weather data stored in the database.
    """
    db_weather = crud.get_latest_hourly_forecast(db, nx, ny)
    if db_weather is None:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return db_weather

@router.get("/weekly", response_model=WeeklyForecastResponse)
def get_weekly_weather(regId: str = "11B10101", db: Session = Depends(get_db)):
    """
    Returns the latest weekly weather data stored in the database.
    """
    db_weekly = crud.get_latest_weekly_forecast(db, regId)
    if db_weekly is None:
        raise HTTPException(status_code=404, detail="Weekly weather data not found")
    return db_weekly

@router.get("/dust", response_model=DustResponse)
def get_dust_info(station_name: str = "종로구", db: Session = Depends(get_db)):
    """
    Returns the latest dust data stored in the database.
    """
    db_dust = crud.get_latest_dust(db, station_name)
    if db_dust is None:
        raise HTTPException(status_code=404, detail="Dust data not found")
    return db_dust

@router.get("/uv", response_model=UVResponse)
def get_uv_info(areaNo: str = "1100000000", db: Session = Depends(get_db)):
    """
    Returns the latest UV data stored in the database.
    """
    db_uv = crud.get_latest_uv(db, areaNo)
    if db_uv is None:
        raise HTTPException(status_code=404, detail="UV data not found")
    return db_uv
