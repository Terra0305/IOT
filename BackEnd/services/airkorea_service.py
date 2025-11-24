import httpx
import os
from fastapi import HTTPException

# AirKorea API Configurations
# Note: This URL might need to be adjusted based on the specific operation (getMsrstnAcctoRltmMesureDnsty)
AIRKOREA_API_URL = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty"
AUTH_KEY = os.getenv("DUST_API_KEY")

async def fetch_dust_info(station_name: str):
    """
    Fetches real-time dust info (PM10, PM2.5) for a specific station.
    """
    if not AUTH_KEY:
        # Fallback to WEATHER_API_KEY if DUST_API_KEY is not separate, or raise error
        # Often keys are shared if from the same portal, but best to have separate env var.
        key = os.getenv("WEATHER_API_KEY")
        if not key:
             raise RuntimeError("DUST_API_KEY (or WEATHER_API_KEY) is not set.")
    else:
        key = AUTH_KEY

    params = {
        "serviceKey": key,
        "returnType": "json",
        "numOfRows": "1",
        "pageNo": "1",
        "stationName": station_name,
        "dataTerm": "DAILY",
        "ver": "1.0"
    }

    async with httpx.AsyncClient() as client:
        try:
            # ServiceKey is often required to be unencoded in some Korean public APIs, 
            # but httpx encodes params by default. If issues arise, might need manual query string construction.
            # For now, we try standard params.
            response = await client.get(AIRKOREA_API_URL, params=params, timeout=10.0)
            
            # Sometimes the API returns XML even if JSON is requested if there's an error key.
            # We'll assume JSON for now.
            
            if response.status_code != 200:
                 raise HTTPException(status_code=response.status_code, detail="AirKorea API Error")

            data = response.json()
            
            # Check for API-level errors
            header = data.get("response", {}).get("header", {})
            if header.get("resultCode") != "00":
                 raise HTTPException(status_code=500, detail=f"AirKorea API Error: {header.get('resultMsg')}")

            items = data.get("response", {}).get("body", {}).get("items", [])
            if not items:
                raise HTTPException(status_code=404, detail="No dust data found for this station.")

            item = items[0]
            
            # Map to our schema
            return {
                "dataTime": item.get("dataTime"),
                "stationName": station_name,
                "pm10Value": item.get("pm10Value"),
                "pm10Grade": item.get("pm10Grade"),
                "pm25Value": item.get("pm25Value"),
                "pm25Grade": item.get("pm25Grade"),
                "khaiValue": item.get("khaiValue"),
                "khaiGrade": item.get("khaiGrade"),
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")
