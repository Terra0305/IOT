import httpx
import os
from sqlalchemy.orm import Session
from models.weather import HourlyForecast, WeeklyForecast, Dust, UV
from utils import get_kst_now, get_vilage_base_time, get_sky_state
from datetime import timedelta

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
VILAGE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
MID_LAND_URL = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst"
MID_TA_URL = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidTa"
DUST_URL = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
UV_URL = "http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4"

async def update_hourly_forecast(db: Session, nx: int = 60, ny: int = 74):
    now = get_kst_now()
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
                print(f"기상청 API 에러: {header.get('resultMsg')}")
                return
            
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
            print(f"[Daily Log] Success: {count} rows inserted/updated.")

        except Exception as e:
            db.rollback()
            print(f"Error logging daily weather: {e}")

async def update_weekly_forecast(
    db: Session, 
    nx: int = 60, 
    ny: int = 74, 
    regId: str = "11F20000", 
    regIdTemp: str = "11F20501"
):
    now = get_kst_now()
    
    if now.hour < 2 or (now.hour == 2 and now.minute < 10):
        base_date = (now - timedelta(days=1)).strftime("%Y%m%d")
        base_time = "2300"
    else:
        base_date = now.strftime("%Y%m%d")
        base_time = "0200"

    print(f"[Weekly Log] Requesting VilageFcst for {base_date} {base_time}")

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
    
    try:
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
        
        db.commit()
        print(f"[Weekly Log] Success: {saved_count} days processed.")
    except Exception as e:
        db.rollback()
        print(f"Error logging weekly weather: {e}")

async def update_dust_info(db: Session, stationName: str = "서석동"):
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
                print("Dust data not found from API")
                return
            
            item = items[0]
            data_time = item.get("dataTime")
            
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
            print(f"[Dust Log] Success: {data_time} {stationName}")

        except Exception as e:
            db.rollback()
            print(f"Error logging dust info: {e}")

async def update_uv_info(db: Session, areaNo: str = "2900000000"):
    now = get_kst_now()
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
            
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            if not items:
                if now.hour < 6:
                     prev_time = (now - timedelta(days=1)).strftime("%Y%m%d") + "18"
                     print(f"[UV Log] Retry with previous day 18:00: {prev_time}")
                     params["time"] = prev_time
                     response = await client.get(UV_URL, params=params, timeout=10.0)
                     data = response.json()
                     items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])

            if not items:
                print("[UV Log] No items found in API response.")
                return
            
            item = items[0]
            date_val = item.get("date")
            
            today_vals = []
            for k in ["h0", "h3", "h6", "h9", "h12", "h15"]:
                val = item.get(k, "0")
                if val and val.isdigit():
                    today_vals.append(int(val))
            
            today_uv = str(max(today_vals)) if today_vals else "0"

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
            print(f"[UV Log] Success: {date_val} {areaNo}")

        except Exception as e:
            db.rollback()
            print(f"Error logging UV info: {e}")
