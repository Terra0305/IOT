import os
import httpx  # API 요청을 위한 라이브러리
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv  # .env 파일을 읽기 위함
from datetime import datetime, timedelta  # base_time 계산용 (timedelta 추가)

# .env 파일에서 환경 변수 로드
load_dotenv()

app = FastAPI()

# 기상청 API URL 및 인증 키
# [수정됨] 기상자료개방포털(apihub.kma.go.kr) URL로 변경
WEATHER_API_URL = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst"
AUTH_KEY = os.getenv("WEATHER_API_KEY")

if not AUTH_KEY:
    raise RuntimeError("WEATHER_API_KEY가 .env 파일에 설정되지 않았습니다!")

@app.get("/api/weather")
async def get_weather(nx: int = 60, ny: int = 127):  # 기본값: 서울특별시 (예시)
    """
    프론트엔드로부터 nx, ny 좌표를 받아 초단기 실황을 반환합니다.
    """
    # --- 기상청 API 요청 파라미터 설정 ---
    # 1. base_date: 오늘 날짜 (예: 20251110)
    now = datetime.now()
    
    # [수정됨] '초단기 실황' (Ncst) API의 base_time 로직
    # - 실황 API는 매시 정각(HH00)에 데이터를 생성하며, 10분 뒤(HH:10)부터 제공됨
    # - 만약 현재 10시 05분이면, 10시 데이터가 아직 없으므로 9시 데이터를 요청해야 함.
    if now.minute < 10:
        # 현재 분이 10분 미만이면, 1시간 전 데이터를 요청
        target_time = now - timedelta(hours=1)
    else:
        # 10분 이후면, 현재 시간의 정각 데이터를 요청
        target_time = now
    
    base_date = target_time.strftime("%Y%m%d")
    base_time = target_time.strftime("%H00")  # '실황' API는 'HH00' 형식 (예: 1000)
    
    # 3. 요청 파라미터 딕셔너리
    params = {
        "authKey": AUTH_KEY,  # [수정됨] serviceKey -> authKey
        "pageNo": 1,
        "numOfRows": 1000,
        "dataType": "JSON",   # JSON으로 받기 (필수!)
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }
    
    # 디버깅용 출력
    print(f"요청 파라미터: base_date={base_date}, base_time={base_time}, nx={nx}, ny={ny}")
    
    # --- httpx를 사용하여 비동기로 기상청 API 호출 ---
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(WEATHER_API_URL, params=params, timeout=10.0)
            
            # 응답 상태 코드 확인
            response.raise_for_status()  # 200 OK가 아니면 예외 발생
            
            # 데이터 반환
            weather_data = response.json()
            
            # API 자체의 에러 응답 확인 (공공데이터 API는 status 200 이어도 에러일 수 있음)
            if weather_data.get("response", {}).get("header", {}).get("resultCode") != "00":
                error_msg = weather_data.get("response", {}).get("header", {}).get("resultMsg", "API Error")
                raise HTTPException(status_code=500, detail=f"기상청 API 에러: {error_msg}")
            
            return weather_data.get("response", {}).get("body", {})
        
        except httpx.HTTPStatusError as e:
            # HTTP 에러 (e.g., 401, 404, 503)
            print(f"HTTP 에러 상세: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP 에러: {e.response.text}")
        
        except httpx.RequestError as e:
            # 네트워크 연결 에러
            raise HTTPException(status_code=503, detail=f"API 요청 중 에러 발생: {e}")
        
        except Exception as e:
            # 기타 예외 (JSON 파싱 실패 등)
            raise HTTPException(status_code=500, detail=f"서버 내부 에러: {str(e)}")

# (참고) uvicorn 실행을 위한 코드 (터미널에서 직접 실행해도 됨)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)