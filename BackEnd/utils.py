from datetime import datetime, timedelta, timezone

def get_kst_now():
    """
    현재 시간을 KST(한국 표준시)로 반환
    - 컨테이너가 UTC일 경우 +9시간
    """
    return datetime.now(timezone.utc) + timedelta(hours=9)

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
