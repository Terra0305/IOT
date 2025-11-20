import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from routers import weather
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services import kma_service, airkorea_service
from database import get_db, SessionLocal
from schemas.weather import HourlyForecastCreate, DustCreate, WeeklyForecastCreate, UVCreate
import crud
import asyncio

# .env 파일 로드 (이미 로드되어 있다고 가정하거나, 필요시 load_dotenv() 호출)
from dotenv import load_dotenv
load_dotenv()

# 스케줄러 생성
scheduler = AsyncIOScheduler()

async def scheduled_weather_log():
    """주기적으로 날씨 데이터를 수집하여 DB에 저장하는 작업"""
    print("[Scheduler] Fetching weather data...")
    try:
        # DB 세션 생성
        db = SessionLocal()
        try:
            # 서울 좌표 (기본값)
            nx, ny = 60, 127
            data = await kma_service.fetch_ultra_srt_ncst(nx, ny)
            weather_create = HourlyForecastCreate(**data)
            crud.create_hourly_forecast(db, weather_create)
            print("[Scheduler] Weather data saved.")
        finally:
            db.close()
    except Exception as e:
        print(f"[Scheduler] Error fetching weather: {e}")

async def scheduled_dust_log():
    """주기적으로 미세먼지 데이터를 수집하여 DB에 저장하는 작업"""
    print("[Scheduler] Fetching dust data...")
    try:
        db = SessionLocal()
        try:
            station_name = "종로구"
            data = await airkorea_service.fetch_dust_info(station_name)
            dust_create = DustCreate(**data)
            crud.create_dust(db, dust_create)
            print("[Scheduler] Dust data saved.")
        finally:
            db.close()
    except Exception as e:
        print(f"[Scheduler] Error fetching dust: {e}")

async def scheduled_weekly_log():
    """주기적으로 주간 예보 데이터를 수집하여 DB에 저장하는 작업 (하루 2회 권장)"""
    print("[Scheduler] Fetching weekly weather data...")
    try:
        db = SessionLocal()
        try:
            # 서울/경기 기준
            regId_temp = "11B10101"
            regId_land = "11B00000"
            data = await kma_service.fetch_mid_term_forecast(regId_temp, regId_land)
            weekly_create = WeeklyForecastCreate(**data)
            crud.create_weekly_forecast(db, weekly_create)
            print("[Scheduler] Weekly weather data saved.")
        finally:
            db.close()
    except Exception as e:
        print(f"[Scheduler] Error fetching weekly weather: {e}")

async def scheduled_uv_log():
    """주기적으로 자외선 데이터를 수집하여 DB에 저장하는 작업"""
    print("[Scheduler] Fetching UV data...")
    try:
        db = SessionLocal()
        try:
            areaNo = "1100000000" # 서울
            data = await kma_service.fetch_uv_index(areaNo)
            uv_create = UVCreate(**data)
            crud.create_uv(db, uv_create)
            print("[Scheduler] UV data saved.")
        finally:
            db.close()
    except Exception as e:
        print(f"[Scheduler] Error fetching UV: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # [시작]
    try:
        init_db()
        print("[System] DB Initialized.")
    except Exception as e:
        print(f"[System] DB Initialization Failed: {e}")
    
    # 스케줄러 시작
    # 1시간마다 실행 (예시)
    scheduler.add_job(scheduled_weather_log, 'interval', minutes=60)
    scheduler.add_job(scheduled_dust_log, 'interval', minutes=60)
    # 중기예보와 자외선은 갱신 주기가 길므로 3시간마다 실행 (예시)
    scheduler.add_job(scheduled_weekly_log, 'interval', minutes=180)
    scheduler.add_job(scheduled_uv_log, 'interval', minutes=180)
    
    scheduler.start()
    print("[System] Scheduler Started.")
    
    yield
    
    # [종료]
    scheduler.shutdown()
    print("[System] Scheduler Shutdown.")

app = FastAPI(lifespan=lifespan)

# 라우터 등록
app.include_router(weather.router)

@app.get("/")
def read_root():
    return {"message": "FastAPI Weather Server is Running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)