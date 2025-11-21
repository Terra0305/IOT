import httpx
import os
from datetime import datetime, timedelta
from fastapi import HTTPException
import asyncio

# KMA API Configurations
# 1. 초단기실황 (Ultra Short-term Nowcast)
KMA_NCST_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
# 2. 단기예보 (Short-term Forecast)
KMA_VILAGE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
# 3. 중기예보 (Mid-term)
KMA_MID_TA_URL = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidTa"
KMA_MID_LAND_URL = "http://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst"
# 4. 자외선 (UV)
KMA_UV_URL = "http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4"

AUTH_KEY = os.getenv("WEATHER_API_KEY")

async def fetch_ultra_srt_ncst(nx: int, ny: int):
    """
    Fetches Ultra Short-term Nowcast (Ncst) from KMA API.
    Returns current weather data.
    """
    if not AUTH_KEY:
        raise RuntimeError("WEATHER_API_KEY is not set.")

    now = datetime.now()
    if now.minute < 40: # API provides data 40 mins after the hour
        target_time = now - timedelta(hours=1)
    else:
        target_time = now

    base_date = target_time.strftime("%Y%m%d")
    base_time = target_time.strftime("%H00")

    params = {
        "serviceKey": AUTH_KEY, 
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
            response = await client.get(KMA_NCST_URL, params=params, timeout=10.0)
            response.raise_for_status()
            
            try:
                data = response.json()
            except:
                raise HTTPException(status_code=500, detail=f"API returned non-JSON: {response.text[:100]}")

            header = data.get("response", {}).get("header", {})
            if header.get("resultCode") != "00":
                raise HTTPException(status_code=500, detail=f"KMA API Error: {header.get('resultMsg')}")

            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            
            result = {
                "base_date": base_date,
                "base_time": base_time,
                "nx": nx,
                "ny": ny
            }
            
            for item in items:
                category = item.get("category")
                value = float(item.get("obsrValue", 0))
                
                if category == "T1H": result["temperature"] = value
                elif category == "REH": result["humidity"] = value
                elif category == "RN1": result["rain_1h"] = value
                elif category == "PTY": result["precip_type"] = int(value)
                elif category == "WSD": result["wind_speed"] = value
                elif category == "VEC": result["wind_direction"] = value
                elif category == "UUU": result["wind_ew"] = value
                elif category == "VVV": result["wind_ns"] = value
            
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")

async def fetch_vilage_fcst(nx: int, ny: int):
    """
    Fetches Short-term Forecast (VilageFcst) from KMA API.
    Returns 24-hour forecast data.
    """
    if not AUTH_KEY:
        raise RuntimeError("WEATHER_API_KEY is not set.")

    # Base time calculation: 02, 05, 08, 11, 14, 17, 20, 23
    # API provides data ~10 mins after base time.
    now = datetime.now()
    
    # Find the latest base time
    # Logic: If now is 13:00, latest base time is 11:00.
    # If now is 02:05, latest base time is 23:00 (yesterday) or 02:00 (if > 02:10)
    # Safe bet: use 1 hour ago and find closest 3-hour block.
    
    # Simple logic:
    # 1. List all base times for today and yesterday
    candidates = []
    for d in [0, 1]: # Today and Yesterday
        date = now - timedelta(days=d)
        for h in [2, 5, 8, 11, 14, 17, 20, 23]:
            dt = date.replace(hour=h, minute=10, second=0, microsecond=0) # +10 mins for safety
            if dt <= now:
                candidates.append(dt)
    
    latest_base = max(candidates)
    # Adjust back to base time (remove 10 mins)
    base_date = latest_base.strftime("%Y%m%d")
    base_time = (latest_base - timedelta(minutes=10)).strftime("%H00")

    params = {
        "serviceKey": AUTH_KEY,
        "pageNo": 1,
        "numOfRows": 1000, # Fetch enough for 24h+
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(KMA_VILAGE_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            if not items:
                raise HTTPException(status_code=404, detail="No forecast data found")

            # Group by fcstDate + fcstTime
            grouped = {}
            for item in items:
                key = (item['fcstDate'], item['fcstTime'])
                if key not in grouped:
                    grouped[key] = {
                        "fcstDate": item['fcstDate'],
                        "fcstTime": item['fcstTime'],
                        "nx": nx,
                        "ny": ny
                    }
                
                cat = item['category']
                val = item['fcstValue']
                
                if cat == "TMP": grouped[key]["temperature"] = float(val)
                elif cat == "REH": grouped[key]["humidity"] = int(val)
                elif cat == "SKY": grouped[key]["sky"] = int(val)
                elif cat == "PTY": grouped[key]["pty"] = int(val)
                elif cat == "POP": grouped[key]["pop"] = int(val)
                elif cat == "PCP": grouped[key]["pcp"] = val
                elif cat == "VEC": grouped[key]["vec"] = float(val)
                elif cat == "WSD": grouped[key]["wsd"] = float(val)

            # Filter for next 24 hours from NOW
            # But user just said "24시간 예측데이터를 저장". 
            # We can just return all valid future data we got (usually ~48h+).
            # Let's return sorted list.
            return sorted(grouped.values(), key=lambda x: (x['fcstDate'], x['fcstTime']))

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Vilage Forecast Error: {str(e)}")

async def fetch_mid_term_forecast(regId_temp: str, regId_land: str, tmFc: str):
    """
    Fetches Mid-term Forecast.
    tmFc: Announcement Time (YYYYMMDDHHMM)
    """
    params_common = {
        "serviceKey": AUTH_KEY,
        "pageNo": 1,
        "numOfRows": 10,
        "dataType": "JSON",
        "tmFc": tmFc
    }

    async with httpx.AsyncClient() as client:
        # 1. Fetch Temperature
        params_temp = params_common.copy()
        params_temp["regId"] = regId_temp
        resp_temp = await client.get(KMA_MID_TA_URL, params=params_temp, timeout=10.0)
        data_temp = resp_temp.json().get("response", {}).get("body", {}).get("items", {}).get("item", [])
        item_temp = data_temp[0] if data_temp else {}

        # 2. Fetch Land Forecast
        params_land = params_common.copy()
        params_land["regId"] = regId_land
        resp_land = await client.get(KMA_MID_LAND_URL, params=params_land, timeout=10.0)
        data_land = resp_land.json().get("response", {}).get("body", {}).get("items", {}).get("item", [])
        item_land = data_land[0] if data_land else {}

        return item_temp, item_land

async def fetch_weekly_weather(nx: int, ny: int, regId_temp: str, regId_land: str):
    """
    Fetches and combines Short-term (Day 1-3) and Mid-term (Day 4-7) forecasts.
    """
    # 1. Fetch Short-term for Day 1-3
    # We reuse fetch_vilage_fcst logic but we need to process it differently.
    # Or just call it and process the result.
    short_term_data = await fetch_vilage_fcst(nx, ny)
    
    # Process Short-term data to get Day 1, 2, 3 summaries
    # Need to map "Today", "Tomorrow", "Day after tomorrow" to Day 1, 2, 3 relative to NOW?
    # Or relative to Announcement Date?
    # User said: "예보날짜는 한국현재시간을 기준으로하여 DB를 업데이트" -> tmFc = Now
    now = datetime.now()
    tmFc = now.strftime("%Y%m%d%H00") # Current hour as announcement time
    
    # Group short term data by Date
    daily_summary = {}
    for item in short_term_data:
        date = item['fcstDate']
        if date not in daily_summary:
            daily_summary[date] = {"temps": [], "pops": [], "skies": []}
        
        if item.get("temperature") is not None: daily_summary[date]["temps"].append(item["temperature"])
        if item.get("pop") is not None: daily_summary[date]["pops"].append(item["pop"])
        # Sky/PTY logic is complex, let's simplify: use SKY.
        if item.get("sky") is not None: daily_summary[date]["skies"].append(item["sky"])

    sorted_dates = sorted(daily_summary.keys())
    
    # 2. Fetch Mid-term for Day 4-7
    # Mid-term requires specific tmFc (0600 or 1800).
    # If now is 14:00, we use today 06:00.
    if now.hour < 6:
        mid_tmFc = (now - timedelta(days=1)).replace(hour=18, minute=0).strftime("%Y%m%d%H%M")
    elif now.hour < 18:
        mid_tmFc = now.replace(hour=6, minute=0).strftime("%Y%m%d%H%M")
    else:
        mid_tmFc = now.replace(hour=18, minute=0).strftime("%Y%m%d%H%M")
        
    mid_temp, mid_land = await fetch_mid_term_forecast(regId_temp, regId_land, mid_tmFc)

    # 3. Combine
    result = {
        "regId": regId_land, # Use Land RegId as primary
        "tmFc": tmFc,
    }

    # Fill Day 1-3 from Short-term
    # Note: sorted_dates[0] is likely Today or Tomorrow depending on time.
    # We need to map them to Day 1, 2, 3.
    # Let's assume Day 1 = Today (or next 24h?), Day 2 = Tomorrow...
    # "1-3일후는 단기예보" -> usually means Day 1 (Tomorrow), Day 2, Day 3.
    # But let's fill what we have.
    
    # Helper to get summary
    def get_day_summary(date_str):
        if date_str not in daily_summary: return None
        d = daily_summary[date_str]
        return {
            "min": min(d["temps"]) if d["temps"] else None,
            "max": max(d["temps"]) if d["temps"] else None,
            "pop_max": max(d["pops"]) if d["pops"] else 0,
            "sky_avg": sum(d["skies"])/len(d["skies"]) if d["skies"] else 0 # Very rough
        }

    # Map dates to Day 1, 2, 3
    # Day 1 = Today? Or Tomorrow?
    # Usually Weekly Forecast starts from "Tomorrow" or "After 3 days" depending on context.
    # User said "1-3일후는 단기예보". Let's assume Day 1 = Tomorrow.
    # If today is 21st, Day 1 = 22nd.
    base_date_obj = now.date()
    
    for i in range(1, 4): # 1, 2, 3
        target_date = (base_date_obj + timedelta(days=i)).strftime("%Y%m%d")
        summary = get_day_summary(target_date)
        if summary:
            result[f"taMin{i}"] = int(summary["min"]) if summary["min"] is not None else None
            result[f"taMax{i}"] = int(summary["max"]) if summary["max"] is not None else None
            result[f"rnSt{i}Am"] = summary["pop_max"] # Simplify: use max pop for both am/pm
            result[f"rnSt{i}Pm"] = summary["pop_max"]
            # Map sky to text
            sky_val = summary["sky_avg"]
            wf = "맑음" if sky_val < 2 else "구름많음" if sky_val < 3.5 else "흐림"
            result[f"wf{i}Am"] = wf
            result[f"wf{i}Pm"] = wf

    # Fill Day 4-7 from Mid-term
    # Mid-term fields: rnSt3Am, rnSt3Pm... wait, Mid-term starts from Day 3 usually.
    # But we are using it for Day 4-7.
    # Mid-term data keys: rnSt3Am, ..., rnSt4Am, ..., rnSt7Am...
    # We map Mid-term's Day 4 to our Day 4.
    for i in range(4, 8): # 4, 5, 6, 7
        result[f"rnSt{i}Am"] = mid_land.get(f"rnSt{i}Am")
        result[f"rnSt{i}Pm"] = mid_land.get(f"rnSt{i}Pm")
        result[f"wf{i}Am"] = mid_land.get(f"wf{i}Am")
        result[f"wf{i}Pm"] = mid_land.get(f"wf{i}Pm")
        result[f"taMin{i}"] = mid_temp.get(f"taMin{i}")
        result[f"taMax{i}"] = mid_temp.get(f"taMax{i}")

    return result

async def fetch_uv_index(areaNo: str):
    """
    Fetches UV Index.
    areaNo: Area Code (e.g., 1100000000 for Seoul)
    """
    if not AUTH_KEY:
        raise RuntimeError("WEATHER_API_KEY is not set.")
        
    now = datetime.now()
    time = now.strftime("%Y%m%d%H")
    
    params = {
        "serviceKey": AUTH_KEY,
        "pageNo": 1,
        "numOfRows": 10,
        "dataType": "JSON",
        "areaNo": areaNo,
        "time": time 
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(KMA_UV_URL, params=params, timeout=10.0)
        data = response.json()
        
        items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
        if not items:
            raise HTTPException(status_code=404, detail="UV Data not found")
            
        item = items[0]
        
        return {
            "date": item.get("date"), # YYYYMMDDHH
            "areaNo": areaNo,
            "today": str(item.get("today")),
            "tomorrow": str(item.get("tomorrow"))
        }
