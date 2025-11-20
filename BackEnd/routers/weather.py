from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import kma_service, airkorea_service
from schemas.weather import HourlyForecastCreate, HourlyForecastResponse, DustCreate, DustResponse, MessageResponse
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
    Fetches current weather from KMA API and saves it to the database.
    """
    try:
        data = await kma_service.fetch_ultra_srt_ncst(nx, ny)
        weather_create = HourlyForecastCreate(**data)
        db_weather = crud.create_hourly_forecast(db, weather_create)
        return db_weather
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

@router.get("/dust", response_model=DustResponse)
def get_dust_info(station_name: str = "종로구", db: Session = Depends(get_db)):
    """
    Returns the latest dust data stored in the database.
    """
    db_dust = crud.get_latest_dust(db, station_name)
    if db_dust is None:
        raise HTTPException(status_code=404, detail="Dust data not found")
    return db_dust
