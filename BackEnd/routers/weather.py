from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.weather import HourlyForecast, WeeklyForecast, Dust, UV
from datetime import datetime, timedelta
import httpx
import os
from utils import get_kst_now, get_vilage_base_time, get_sky_state
from services.weather_scheduler_service import (
    update_hourly_forecast, 
    update_weekly_forecast, 
    update_dust_info, 
    update_uv_info
)

router = APIRouter(
    prefix="/api/weather",
    tags=["weather"],
    responses={404: {"description": "Not found"}},
)

# API Key & URLs
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NCST_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
SRT_FCST_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"

@router.get("/current")
async def get_current_weather(nx: int = 60, ny: int = 74, db: Session = Depends(get_db)):
    """
    [Read] 현재 날씨 조회 (초단기실황 + 초단기예보 + DB 주간예보)
    - PTY, T1H 등: 초단기실황 (NCST)
    - SKY: 초단기예보 (SRT_FCST)
    - TMX, TMN: DB WeeklyForecast (오늘 날짜)
    """
    now = get_kst_now()
    # 1. Base Time 계산 (초단기실황/예보 공용)
    # 매시 45분 이후에 호출 가능 -> 40분 이전이면 1시간 전 base_time 사용
    if now.minute < 45:
        target = now - timedelta(hours=1)
    else:
        target = now

    base_date = target.strftime("%Y%m%d")
    base_time = target.strftime("%H00")

    params = {
        "serviceKey": WEATHER_API_KEY,
        "pageNo": 1,
        "numOfRows": 100,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }

    result = {}

    async with httpx.AsyncClient() as client:
        try:
            # 2. 초단기실황 (NCST) 호출 -> PTY, T1H, RN1, REH, UUU, VVV, VEC, WSD
            resp_ncst = await client.get(NCST_URL, params=params, timeout=10.0)
            resp_ncst.raise_for_status()
            data_ncst = resp_ncst.json()
            items_ncst = data_ncst.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            
            for item in items_ncst:
                result[item["category"]] = item["obsrValue"]

            # 3. 초단기예보 (SRT_FCST) 호출 -> SKY
            resp_fcst = await client.get(SRT_FCST_URL, params=params, timeout=10.0)
            resp_fcst.raise_for_status()
            data_fcst = resp_fcst.json()
            items_fcst = data_fcst.get("response", {}).get("body", {}).get("items", {}).get("item", [])

            # 가장 빠른 예보 시간의 SKY 값 찾기
            # items는 fcstTime, fcstDate 순으로 정렬되어 있다고 가정
            # SKY 카테고리의 첫 번째 값을 사용
            for item in items_fcst:
                if item["category"] == "SKY":
                    result["SKY"] = item["fcstValue"]
                    break # 가장 빠른 시간의 SKY만 취함

            # 4. DB에서 오늘 날짜의 최고/최저 기온 조회
            today_str = now.strftime("%Y%m%d")
            weekly_row = db.query(WeeklyForecast).filter(WeeklyForecast.fcstDate == today_str).first()
            
            if weekly_row:
                result["TMX"] = weekly_row.taMax
                result["TMN"] = weekly_row.taMin
            else:
                result["TMX"] = None
                result["TMN"] = None

            return {
                "base_date": base_date,
                "base_time": base_time,
                "weather": result
            }

        except Exception as e:
            print(f"Error fetching current weather: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@router.post("/log/daily")
async def log_daily_weather(nx: int = 60, ny: int = 74, db: Session = Depends(get_db)):
    """
    [Write] 단기예보(24시간) 데이터 수집 및 DB 저장
    - HourlyForecast 테이블 업데이트
    """
    try:
        await update_hourly_forecast(db, nx, ny)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/daily")
async def get_daily_weather(nx: int = 60, ny: int = 74, db: Session = Depends(get_db)):
    """
    [Read] 저장된 단기예보 조회
    """
    now_str = get_kst_now().strftime("%Y%m%d")
    
    results = db.query(HourlyForecast).filter(
        HourlyForecast.nx == nx,
        HourlyForecast.ny == ny,
        HourlyForecast.base_date >= now_str 
    ).order_by(HourlyForecast.base_date, HourlyForecast.base_time).all()
    
    return results

@router.post("/log/weekly")
async def log_weekly_weather(
    nx: int = 60, 
    ny: int = 74, 
    regId: str = "11F20000", 
    regIdTemp: str = "11F20501", 
    db: Session = Depends(get_db)
):
    """
    [Write] 주간 예보 데이터 수집 및 저장 (Day 0~7)
    """
    try:
        await update_weekly_forecast(db, nx, ny, regId, regIdTemp)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weekly")
async def get_weekly_weather(regId: str = "11F20000", db: Session = Depends(get_db)):
    """
    [Read] 주간 예보 조회
    """
    now_str = get_kst_now().strftime("%Y%m%d")
    
    results = db.query(WeeklyForecast).filter(
        WeeklyForecast.regId == regId,
        WeeklyForecast.fcstDate >= now_str
    ).order_by(WeeklyForecast.fcstDate).all()
    
    return results

# --- Dust (Fine Dust) APIs ---

@router.post("/log/dust")
async def log_dust_info(stationName: str = "서석동", db: Session = Depends(get_db)):
    """
    [Write] 미세먼지 데이터 수집 및 저장
    """
    try:
        await update_dust_info(db, stationName)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dust")
async def get_dust_info(stationName: str = "서석동", db: Session = Depends(get_db)):
    """
    [Read] 최신 미세먼지 데이터 조회
    """
    result = db.query(Dust).filter_by(stationName=stationName).order_by(Dust.dataTime.desc()).first()
    if not result:
        raise HTTPException(status_code=404, detail="Dust data not found in DB")
    return result

# --- UV (Ultraviolet) APIs ---

@router.post("/log/uv")
async def log_uv_info(areaNo: str = "2900000000", db: Session = Depends(get_db)):
    """
    [Write] 자외선 지수 데이터 수집 및 저장
    """
    try:
        await update_uv_info(db, areaNo)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/uv")
async def get_uv_info(areaNo: str = "2900000000", db: Session = Depends(get_db)):
    """
    [Read] 최신 자외선 지수 조회
    """
    result = db.query(UV).filter_by(areaNo=areaNo).order_by(UV.date.desc()).first()
    if not result:
        raise HTTPException(status_code=404, detail="UV data not found in DB")
    return result
