import httpx
import os
from datetime import datetime, timedelta
from fastapi import HTTPException

# KMA API Configurations
# 1. 단기예보 (Short-term)
KMA_NCST_URL = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst"
# 2. 중기예보 (Mid-term)
KMA_MID_TA_URL = "https://apis.data.go.kr/1360000/MidFcstInfoService/getMidTa"
KMA_MID_LAND_URL = "https://apis.data.go.kr/1360000/MidFcstInfoService/getMidLandFcst"
# 3. 자외선 (UV)
KMA_UV_URL = "https://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4"

AUTH_KEY = os.getenv("WEATHER_API_KEY")

async def fetch_ultra_srt_ncst(nx: int, ny: int):
    """
    Fetches Ultra Short-term Nowcast (Ncst) from KMA API.
    """
    if not AUTH_KEY:
        raise RuntimeError("WEATHER_API_KEY is not set.")

    now = datetime.now()
    if now.minute < 10:
        target_time = now - timedelta(hours=1)
    else:
        target_time = now

    base_date = target_time.strftime("%Y%m%d")
    base_time = target_time.strftime("%H00")

    params = {
        "authKey": AUTH_KEY, # Note: Some APIs use 'serviceKey', others 'authKey'. Check docs.
        # Public Data Portal usually uses 'serviceKey'. APIHub uses 'authKey'.
        # The user provided a Public Data Portal key. 
        # IF using Public Data Portal URL for Short-term:
        # URL: http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst
        # Param: serviceKey
        # The current URL in code is APIHUB (apihub.kma.go.kr). 
        # We should probably switch to Public Data Portal URL for consistency if the key is from there.
        # Let's try to support both or switch to Public Data Portal URL.
        # SWITCHING TO PUBLIC DATA PORTAL URL for Short-term as well to match the key source.
        "serviceKey": AUTH_KEY, 
        "pageNo": 1,
        "numOfRows": 1000,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }
    
    # Update URL to Public Data Portal
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            # print(f"Request URL: {response.url}") # Debug
            response.raise_for_status()
            
            try:
                data = response.json()
            except:
                # Sometimes it returns XML on error even if JSON requested
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

async def fetch_mid_term_forecast(regId_temp: str, regId_land: str):
    """
    Fetches Mid-term Forecast (Temperature & Land).
    regId_temp: Region ID for temperature (e.g., 11B10101 for Seoul)
    regId_land: Region ID for land weather (e.g., 11B00000 for Seoul/Gyeonggi)
    """
    if not AUTH_KEY:
        raise RuntimeError("WEATHER_API_KEY is not set.")

    # Mid-term forecast is announced at 06:00 and 18:00 daily.
    now = datetime.now()
    if now.hour < 6:
        # Use yesterday 18:00
        target_time = (now - timedelta(days=1)).replace(hour=18, minute=0, second=0, microsecond=0)
    elif now.hour < 18:
        # Use today 06:00
        target_time = now.replace(hour=6, minute=0, second=0, microsecond=0)
    else:
        # Use today 18:00
        target_time = now.replace(hour=18, minute=0, second=0, microsecond=0)
        
    tmFc = target_time.strftime("%Y%m%d%H%M") # YYYYMMDDHHMM

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
        if not data_temp:
             # Fallback or error handling
             pass
        item_temp = data_temp[0] if data_temp else {}

        # 2. Fetch Land Forecast
        params_land = params_common.copy()
        params_land["regId"] = regId_land
        
        resp_land = await client.get(KMA_MID_LAND_URL, params=params_land, timeout=10.0)
        data_land = resp_land.json().get("response", {}).get("body", {}).get("items", {}).get("item", [])
        item_land = data_land[0] if data_land else {}

        # Combine results (Mapping to WeeklyForecast Schema)
        # Note: Schema needs to be flexible or we map specific fields.
        # For now, let's return a dict that matches our WeeklyForecastBase schema.
        
        return {
            "tmFc": tmFc,
            "regId": regId_temp, # Using temp regId as primary for now
            "rnSt3Am": item_land.get("rnSt3Am"),
            "rnSt3Pm": item_land.get("rnSt3Pm"),
            "wf3Am": item_land.get("wf3Am"),
            "wf3Pm": item_land.get("wf3Pm"),
            "taMin3": item_temp.get("taMin3"),
            "taMax3": item_temp.get("taMax3"),
            # Add more days if needed
        }

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
