import httpx
import os
from datetime import datetime, timedelta
from fastapi import HTTPException

# KMA API Configurations
KMA_NCST_URL = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst"
AUTH_KEY = os.getenv("WEATHER_API_KEY")

async def fetch_ultra_srt_ncst(nx: int, ny: int):
    """
    Fetches Ultra Short-term Nowcast (Ncst) from KMA API.
    """
    if not AUTH_KEY:
        raise RuntimeError("WEATHER_API_KEY is not set in environment variables.")

    now = datetime.now()
    # API provides data for HH:00 after HH:10 (approx)
    if now.minute < 10:
        target_time = now - timedelta(hours=1)
    else:
        target_time = now

    base_date = target_time.strftime("%Y%m%d")
    base_time = target_time.strftime("%H00")

    params = {
        "authKey": AUTH_KEY,
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
            data = response.json()
            
            header = data.get("response", {}).get("header", {})
            if header.get("resultCode") != "00":
                raise HTTPException(status_code=500, detail=f"KMA API Error: {header.get('resultMsg')}")

            items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
            
            # Transform list of items into a dictionary for easier access
            # Item format: {'category': 'T1H', 'obsrValue': '18.5', ...}
            result = {
                "base_date": base_date,
                "base_time": base_time,
                "nx": nx,
                "ny": ny
            }
            
            for item in items:
                category = item.get("category")
                value = float(item.get("obsrValue", 0))
                
                if category == "T1H": # Temperature
                    result["temperature"] = value
                elif category == "REH": # Humidity
                    result["humidity"] = value
                elif category == "RN1": # 1h Rain
                    result["rain_1h"] = value
                elif category == "PTY": # Precip Type
                    result["precip_type"] = int(value)
                elif category == "WSD": # Wind Speed
                    result["wind_speed"] = value
                elif category == "VEC": # Wind Direction
                    result["wind_direction"] = value
                elif category == "UUU": # Wind EW
                    result["wind_ew"] = value
                elif category == "VVV": # Wind NS
                    result["wind_ns"] = value
            
            return result

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP Error: {e.response.text}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Request Error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")
