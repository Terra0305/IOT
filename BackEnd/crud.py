from sqlalchemy.orm import Session
from models.weather import HourlyForecast, WeeklyForecast, Dust, UV
from schemas.weather import HourlyForecastCreate, DustCreate, UVCreate

# --- Hourly Forecast ---
def create_hourly_forecast(db: Session, forecast: HourlyForecastCreate):
    # Upsert: Check if exists, if so update, else insert
    db_obj = db.query(HourlyForecast).filter(
        HourlyForecast.base_date == forecast.base_date,
        HourlyForecast.base_time == forecast.base_time,
        HourlyForecast.nx == forecast.nx,
        HourlyForecast.ny == forecast.ny
    ).first()

    if db_obj:
        # Update existing
        for key, value in forecast.dict().items():
            setattr(db_obj, key, value)
    else:
        # Create new
        db_obj = HourlyForecast(**forecast.dict())
        db.add(db_obj)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_latest_hourly_forecast(db: Session, nx: int, ny: int):
    return db.query(HourlyForecast).filter(
        HourlyForecast.nx == nx,
        HourlyForecast.ny == ny
    ).order_by(HourlyForecast.base_date.desc(), HourlyForecast.base_time.desc()).first()

# --- Dust ---
def create_dust(db: Session, dust: DustCreate):
    db_obj = db.query(Dust).filter(
        Dust.dataTime == dust.dataTime,
        Dust.stationName == dust.stationName
    ).first()

    if db_obj:
        for key, value in dust.dict().items():
            setattr(db_obj, key, value)
    else:
        db_obj = Dust(**dust.dict())
        db.add(db_obj)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_latest_dust(db: Session, station_name: str):
    return db.query(Dust).filter(
        Dust.stationName == station_name
    ).order_by(Dust.dataTime.desc()).first()

# --- UV ---
def create_uv(db: Session, uv: UVCreate):
    db_obj = db.query(UV).filter(
        UV.date == uv.date,
        UV.areaNo == uv.areaNo
    ).first()

    if db_obj:
        for key, value in uv.dict().items():
            setattr(db_obj, key, value)
    else:
        db_obj = UV(**uv.dict())
        db.add(db_obj)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_latest_uv(db: Session, area_no: str):
    return db.query(UV).filter(
        UV.areaNo == area_no
    ).order_by(UV.date.desc()).first()

# --- Weekly Forecast ---
def create_weekly_forecast(db: Session, forecast: WeeklyForecastCreate):
    db_obj = db.query(WeeklyForecast).filter(
        WeeklyForecast.tmFc == forecast.tmFc,
        WeeklyForecast.regId == forecast.regId
    ).first()

    if db_obj:
        for key, value in forecast.dict().items():
            setattr(db_obj, key, value)
    else:
        db_obj = WeeklyForecast(**forecast.dict())
        db.add(db_obj)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_latest_weekly_forecast(db: Session, reg_id: str):
    return db.query(WeeklyForecast).filter(
        WeeklyForecast.regId == reg_id
    ).order_by(WeeklyForecast.tmFc.desc()).first()
