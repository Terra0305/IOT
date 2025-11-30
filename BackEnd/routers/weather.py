from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.weather import HourlyForecast, WeeklyForecast, Dust, UV
from datetime import datetime, timedelta
import httpx
import os

router = APIRouter(
    prefix="/api/weather",
    tags=["weather"],
    responses={404: {"description": "Not found"}},
)

# API Key & URLs
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NCST_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
SRT_FCST_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
VILAGE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
MID_LAND_URL = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst"
MID_TA_URL = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidTa"
DUST_URL = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
UV_URL = "http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4"

def get_vilage_base_time(now: datetime):
    """
    단기예보(VilageFcst) Base Time 계산
    - Base Time: 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 (1일 8회)
    - API 제공은 Base Time + 10분 뒤부터
    """
    base_times = [2, 5, 8, 11, 14, 17, 20, 23]
    target = now - timedelta(minutes=10)
    found_hour = None
    for hour in reversed(base_times):
        if target.hour >= hour:
            found_hour = hour
            break
    
    if found_hour is None:
        target_date = target - timedelta(days=1)
        return target_date.strftime("%Y%m%d"), "2300"
    else:
        return target.strftime("%Y%m%d"), f"{found_hour:02d}00"

def get_sky_state(sky_code, pty_code):
    """단기예보 코드를 사람이 읽을 수 있는 날씨로 변환"""
    if pty_code == 1: return "비"
    if pty_code == 2: return "비/눈"
    if pty_code == 3: return "눈"
    if pty_code == 4: return "소나기"
    if sky_code == 1: return "맑음"
    if sky_code == 3: return "구름많음"
    if sky_code == 4: return "흐림"
    return "알수없음"

@router.get("/current")
async def get_current_weather(nx: int = 60, ny: int = 127, db: Session = Depends(get_db)):
    """
    [Read] 현재 날씨 조회 (초단기실황 + 초단기예보 + DB 주간예보)
    - PTY, T1H 등: 초단기실황 (NCST)
    - SKY: 초단기예보 (SRT_FCST)
    - TMX, TMN: DB WeeklyForecast (오늘 날짜)
    """
    now = datetime.now()
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
async def log_daily_weather(nx: int = 60, ny: int = 127, db: Session = Depends(get_db)):
    """
    [Write] 단기예보(24시간) 데이터 수집 및 DB 저장
    - HourlyForecast 테이블 업데이트
    """
    now = datetime.now()
    base_date, base_time = get_vilage_base_time(now)
    
    print(f"[Daily Log] Requesting VilageFcst for {base_date} {base_time}")

    params = {
        "serviceKey": WEATHER_API_KEY,
        "pageNo": 1,
        "numOfRows": 1000,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(VILAGE_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            header = data.get("response", {}).get("header", {})
            if header.get("resultCode") != "00":
                raise HTTPException(status_code=500, detail=f"기상청 API 에러: {header.get('resultMsg')}")
            
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            
            grouped = {}
            for item in items:
                fcst_date = item["fcstDate"]
                fcst_time = item["fcstTime"]
                cat = item["category"]
                val = item["fcstValue"]
                
                key = (fcst_date, fcst_time)
                if key not in grouped:
                    grouped[key] = {}
                grouped[key][cat] = val

            count = 0
            for (f_date, f_time), vals in grouped.items():
                existing = db.query(HourlyForecast).filter_by(
                    base_date=f_date, 
                    base_time=f_time,
                    nx=nx,
                    ny=ny
                ).first()
                
                if not existing:
                    existing = HourlyForecast(
                        base_date=f_date,
                        base_time=f_time,
                        nx=nx,
                        ny=ny
                    )
                    db.add(existing)
                
                existing.temperature = float(vals.get("TMP", 0))
                existing.humidity = float(vals.get("REH", 0))
                
                rn1 = vals.get("PCP", "0")
                if rn1 == "강수없음": rn1 = "0"
                try:
                    existing.rain_1h = float(rn1.replace("mm", ""))
                except:
                    existing.rain_1h = 0.0
                    
                existing.precip_type = int(vals.get("PTY", 0))
                existing.wind_speed = float(vals.get("WSD", 0))
                existing.wind_direction = float(vals.get("VEC", 0))
                existing.wind_ew = float(vals.get("UUU", 0))
                existing.wind_ns = float(vals.get("VVV", 0))
                existing.sky_code = int(vals.get("SKY", 0))
                
                count += 1
            
            db.commit()
            return {"status": "success", "inserted_rows": count, "base_info": f"{base_date} {base_time}"}

        except Exception as e:
            db.rollback()
            print(f"Error logging daily weather: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/daily")
async def get_daily_weather(nx: int = 60, ny: int = 127, db: Session = Depends(get_db)):
    """
    [Read] 저장된 단기예보 조회
    """
    now_str = datetime.now().strftime("%Y%m%d")
    
    results = db.query(HourlyForecast).filter(
        HourlyForecast.nx == nx,
        HourlyForecast.ny == ny,
        HourlyForecast.base_date >= now_str 
    ).order_by(HourlyForecast.base_date, HourlyForecast.base_time).all()
    
    return results

@router.post("/log/weekly")
async def log_weekly_weather(
    nx: int = 60, 
    ny: int = 127, 
    regId: str = "11B00000", 
    regIdTemp: str = "11B10101", 
    db: Session = Depends(get_db)
):
    """
    [Write] 주간 예보 데이터 수집 및 저장 (Day 0~7)
    작동 당일 4일차 정보 누락 문제 있음(API문제라 해결 불가)
    작동 이틀차 부터는 정보 공백 사라짐
    """
    now = datetime.now()
    
    # 1. 단기예보 데이터 가져오기 (Day 0~2)
    # 주간 예보 저장을 위해 Day 0의 오전 데이터(TMN, 0600 날씨 등)가 필요하므로
    # 최신 Base Time 대신 '0200' (또는 전날 2300) Base Time을 고정적으로 사용
    if now.hour < 2 or (now.hour == 2 and now.minute < 10):
        base_date = (now - timedelta(days=1)).strftime("%Y%m%d")
        base_time = "2300"
    else:
        base_date = now.strftime("%Y%m%d")
        base_time = "0200"

    print(f"[Weekly Log] Requesting VilageFcst for {base_date} {base_time} (Fixed for Daily Summary)")

    params_vilage = {
        "serviceKey": WEATHER_API_KEY, 
        "pageNo": 1, "numOfRows": 1000, "dataType": "JSON",
        "base_date": base_date, "base_time": base_time, "nx": nx, "ny": ny
    }
    
    short_term_data = {}

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(VILAGE_URL, params=params_vilage, timeout=10.0)
            resp.raise_for_status()
            items = resp.json().get("response", {}).get("body", {}).get("items", {}).get("item", [])
            
            for item in items:
                f_date = item["fcstDate"]
                f_time = item["fcstTime"]
                cat = item["category"]
                val = item["fcstValue"]
                
                if f_date not in short_term_data:
                    short_term_data[f_date] = {"min": 999, "max": -999, "am_sky": 0, "am_pty": 0, "pm_sky": 0, "pm_pty": 0, "am_pop": 0, "pm_pop": 0}
                
                if cat == "TMN": short_term_data[f_date]["min"] = float(val)
                if cat == "TMX": short_term_data[f_date]["max"] = float(val)
                
                if f_time == "0600":
                    if cat == "SKY": short_term_data[f_date]["am_sky"] = int(val)
                    if cat == "PTY": short_term_data[f_date]["am_pty"] = int(val)
                    if cat == "POP": short_term_data[f_date]["am_pop"] = int(val)
                
                if f_time == "1500":
                    if cat == "SKY": short_term_data[f_date]["pm_sky"] = int(val)
                    if cat == "PTY": short_term_data[f_date]["pm_pty"] = int(val)
                    if cat == "POP": short_term_data[f_date]["pm_pop"] = int(val)

        except Exception as e:
            print(f"[Weekly] Short-term fetch error: {e}")

        tmFc = now.strftime("%Y%m%d") + ("0600" if now.hour < 18 else "1800")
        
        mid_land_params = {"serviceKey": WEATHER_API_KEY, "pageNo": 1, "numOfRows": 10, "dataType": "JSON", "regId": regId, "tmFc": tmFc}
        mid_ta_params = {"serviceKey": WEATHER_API_KEY, "pageNo": 1, "numOfRows": 10, "dataType": "JSON", "regId": regIdTemp, "tmFc": tmFc}
        
        mid_land_data = {}
        mid_ta_data = {}
        
        try:
            resp_land = await client.get(MID_LAND_URL, params=mid_land_params, timeout=10.0)
            mid_land_items = resp_land.json().get("response", {}).get("body", {}).get("items", {}).get("item", [])
            if mid_land_items: mid_land_data = mid_land_items[0]

            resp_ta = await client.get(MID_TA_URL, params=mid_ta_params, timeout=10.0)
            mid_ta_items = resp_ta.json().get("response", {}).get("body", {}).get("items", {}).get("item", [])
            if mid_ta_items: mid_ta_data = mid_ta_items[0]

        except Exception as e:
            print(f"[Weekly] Mid-term fetch error: {e}")

    saved_count = 0
    
    for i in range(8):
        target_date = (now + timedelta(days=i)).strftime("%Y%m%d")
        
        weekly_row = db.query(WeeklyForecast).filter_by(regId=regId, fcstDate=target_date).first()
        if not weekly_row:
            weekly_row = WeeklyForecast(regId=regId, fcstDate=target_date)
            db.add(weekly_row)
        
        if i <= 2: 
            if target_date in short_term_data:
                d = short_term_data[target_date]
                weekly_row.rnStAm = d["am_pop"]
                weekly_row.rnStPm = d["pm_pop"]
                weekly_row.wfAm = get_sky_state(d["am_sky"], d["am_pty"])
                weekly_row.wfPm = get_sky_state(d["pm_sky"], d["pm_pty"])
                weekly_row.taMin = int(d["min"]) if d["min"] != 999 else None
                weekly_row.taMax = int(d["max"]) if d["max"] != -999 else None
        else: 
            idx = i
            if idx <= 7:
                weekly_row.rnStAm = mid_land_data.get(f"rnSt{idx}Am")
                weekly_row.rnStPm = mid_land_data.get(f"rnSt{idx}Pm")
                weekly_row.wfAm = mid_land_data.get(f"wf{idx}Am")
                weekly_row.wfPm = mid_land_data.get(f"wf{idx}Pm")
                weekly_row.taMin = mid_ta_data.get(f"taMin{idx}")
                weekly_row.taMax = mid_ta_data.get(f"taMax{idx}")

        saved_count += 1
    
    try:
        db.commit()
        return {"status": "success", "days_processed": saved_count}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB Error: {e}")

@router.get("/weekly")
async def get_weekly_weather(regId: str = "11B00000", db: Session = Depends(get_db)):
    """
    [Read] 주간 예보 조회
    """
    now_str = datetime.now().strftime("%Y%m%d")
    
    results = db.query(WeeklyForecast).filter(
        WeeklyForecast.regId == regId,
        WeeklyForecast.fcstDate >= now_str
    ).order_by(WeeklyForecast.fcstDate).all()
    
    return results

# --- Dust (Fine Dust) APIs ---

@router.post("/log/dust")
async def log_dust_info(stationName: str = "종로구", db: Session = Depends(get_db)):
    """
    [Write] 미세먼지 데이터 수집 및 저장
    - 에어코리아 API (getMsrstnAcctoRltmMesureDnsty)
    """
    params = {
        "serviceKey": WEATHER_API_KEY,
        "returnType": "json",
        "numOfRows": 1,
        "pageNo": 1,
        "stationName": stationName,
        "dataTerm": "DAILY",
        "ver": "1.0"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(DUST_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            items = data.get("response", {}).get("body", {}).get("items", [])
            if not items:
                raise HTTPException(status_code=404, detail="Dust data not found from API")
            
            item = items[0]
            data_time = item.get("dataTime")
            
            # DB 저장
            dust_row = db.query(Dust).filter_by(dataTime=data_time, stationName=stationName).first()
            if not dust_row:
                dust_row = Dust(dataTime=data_time, stationName=stationName)
                db.add(dust_row)
            
            dust_row.pm10Value = item.get("pm10Value", "-")
            dust_row.pm10Grade = item.get("pm10Grade", "-")
            dust_row.pm25Value = item.get("pm25Value", "-")
            dust_row.pm25Grade = item.get("pm25Grade", "-")
            dust_row.khaiValue = item.get("khaiValue", "-")
            dust_row.khaiGrade = item.get("khaiGrade", "-")
            
            db.commit()
            return {"status": "success", "dataTime": data_time, "stationName": stationName}

        except Exception as e:
            db.rollback()
            print(f"Error logging dust info: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/dust")
async def get_dust_info(stationName: str = "종로구", db: Session = Depends(get_db)):
    """
    [Read] 최신 미세먼지 데이터 조회
    """
    result = db.query(Dust).filter_by(stationName=stationName).order_by(Dust.dataTime.desc()).first()
    if not result:
        raise HTTPException(status_code=404, detail="Dust data not found in DB")
    return result

# --- UV (Ultraviolet) APIs ---

@router.post("/log/uv")
async def log_uv_info(areaNo: str = "1100000000", db: Session = Depends(get_db)):
    """
    [Write] 자외선 지수 데이터 수집 및 저장
    - 기상청 생활기상지수 API (getUVIdxV4)
    - 발표시간: 06시, 18시 (하루 2회)
    - 따라서 요청 시 '오늘 날짜 + 0600'으로 고정해서 요청해야 데이터가 있을 가능성이 높음
    """
    now = datetime.now()
    # 자외선 지수는 06시, 18시에 발표되므로, 안전하게 오늘 날짜의 06시로 요청
    time_str = now.strftime("%Y%m%d") + "06"
    
    print(f"[UV Log] Requesting UV Index for {time_str}, Area: {areaNo}")
    
    params = {
        "serviceKey": WEATHER_API_KEY,
        "pageNo": 1,
        "numOfRows": 10,
        "dataType": "JSON",
        "areaNo": areaNo,
        "time": time_str 
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(UV_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            # 디버깅을 위해 응답 내용 출력
            print(f"[UV Log] Response: {data}")
            
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            if not items:
                # 06시 데이터가 없으면 전날 18시 데이터 시도 (혹시 06시 이전일 경우)
                if now.hour < 6:
                     prev_time = (now - timedelta(days=1)).strftime("%Y%m%d") + "18"
                     print(f"[UV Log] Retry with previous day 18:00: {prev_time}")
                     params["time"] = prev_time
                     response = await client.get(UV_URL, params=params, timeout=10.0)
                     data = response.json()
                     items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])

            if not items:
                print("[UV Log] No items found in API response.")
                raise HTTPException(status_code=404, detail="UV data not found from API")
            
            item = items[0]
            date_val = item.get("date") # 발표시각 (YYYYMMDDHH)
            
            # 데이터 파싱 (h0, h3, ... h75)
            # 오늘: 06시 발표 기준 h0(06시) ~ h15(21시) 중 최대값
            today_vals = []
            for k in ["h0", "h3", "h6", "h9", "h12", "h15"]:
                val = item.get(k, "0")
                if val and val.isdigit():
                    today_vals.append(int(val))
            
            today_uv = str(max(today_vals)) if today_vals else "0"

            # 내일: 06시 발표 기준 h18(내일 00시) ~ h39(내일 21시) 중 최대값
            tomorrow_vals = []
            for k in ["h18", "h21", "h24", "h27", "h30", "h33", "h36", "h39"]:
                val = item.get(k, "0")
                if val and val.isdigit():
                    tomorrow_vals.append(int(val))
            
            tomorrow_uv = str(max(tomorrow_vals)) if tomorrow_vals else "0"

            uv_row = db.query(UV).filter_by(date=date_val, areaNo=areaNo).first()
            if not uv_row:
                uv_row = UV(date=date_val, areaNo=areaNo)
                db.add(uv_row)
            
            uv_row.today = today_uv
            uv_row.tomorrow = tomorrow_uv
            
            db.commit()
            return {
                "status": "success", 
                "date": date_val, 
                "areaNo": areaNo, 
                "today_max": today_uv, 
                "tomorrow_max": tomorrow_uv
            }

        except Exception as e:
            db.rollback()
            print(f"Error logging UV info: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/uv")
async def get_uv_info(areaNo: str = "1100000000", db: Session = Depends(get_db)):
    """
    [Read] 최신 자외선 지수 조회
    """
    result = db.query(UV).filter_by(areaNo=areaNo).order_by(UV.date.desc()).first()
    if not result:
        raise HTTPException(status_code=404, detail="UV data not found in DB")
    return result
