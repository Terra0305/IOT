import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import init_db, SessionLocal
from services.weather_scheduler_service import (
    update_hourly_forecast,
    update_weekly_forecast,
    update_dust_info,
    update_uv_info
)
import asyncio
from led_manager import LEDManager

scheduler = AsyncIOScheduler()
led_manager = LEDManager()

async def update_all_weather_data():
    print("[Scheduler] Starting daily weather update...")
    db = SessionLocal()
    try:
        await update_hourly_forecast(db)
        await update_weekly_forecast(db)
        await update_dust_info(db)
        await update_uv_info(db)
        print("[Scheduler] Daily weather update completed.")
    except Exception as e:
        print(f"[Scheduler] Error during daily update: {e}")
    finally:
        db.close()

async def update_led_status():
    print("[Scheduler] Updating LED status...")
    db = SessionLocal()
    try:
        led_manager.update_weather_status(db)
    except Exception as e:
        print(f"[Scheduler] Error updating LED: {e}")
    finally:
        db.close()

async def main():
    print("[Scheduler Process] Initializing DB...")
    init_db()
    
    print("[Scheduler Process] Starting Scheduler...")
    kst = pytz.timezone('Asia/Seoul')
    scheduler.add_job(update_all_weather_data, 'cron', hour=8, minute=0, timezone=kst)
    scheduler.add_job(update_all_weather_data, 'cron', hour=8, minute=0, timezone=kst)
    # Schedule LED update every 10 minutes
    scheduler.add_job(update_led_status, 'interval', minutes=10, timezone=kst)
    
    scheduler.start()
    
    # Start LED Heartbeat (runs in background)
    asyncio.create_task(led_manager.start_heartbeat())
    
    # Initial LED update
    await update_led_status()
    print("[Scheduler Process] Scheduler started. Job scheduled for 08:00 KST daily.")
    
    # Keep alive
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
