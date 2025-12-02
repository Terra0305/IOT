import asyncio
import os
import logging
from sqlalchemy.orm import Session
from models.weather import HourlyForecast, Dust
from utils import get_kst_now

# Configure logging
logger = logging.getLogger("LEDManager")
logger.setLevel(logging.INFO)

# Try importing RPi.GPIO, use mock if not available (e.g., dev environment)
try:
    import RPi.GPIO as GPIO
    IS_RPI = True
except ImportError:
    IS_RPI = False
    logger.warning("RPi.GPIO not found. Running in Mock mode.")
    
    # Mock GPIO class
    class MockGPIO:
        BCM = "BCM"
        OUT = "OUT"
        HIGH = "HIGH"
        LOW = "LOW"
        def setmode(self, mode): pass
        def setup(self, pin, mode): pass
        def output(self, pin, state): pass # print(f"[MockGPIO] Pin {pin} -> {state}")
        def cleanup(self): pass
        def setwarnings(self, state): pass
    
    GPIO = MockGPIO()

class LEDManager:
    # GPIO Pin Constants (BCM)
    PIN_GREEN = 17
    PIN_RED = 27
    PIN_YELLOW = 22

    def __init__(self):
        self.running = False
        self._setup_gpio()

    def _setup_gpio(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(self.PIN_GREEN, GPIO.OUT)
            GPIO.setup(self.PIN_RED, GPIO.OUT)
            GPIO.setup(self.PIN_YELLOW, GPIO.OUT)
            
            # Initial state: All OFF
            self._all_off()
            logger.info("GPIO Setup Complete.")
        except Exception as e:
            logger.error(f"GPIO Setup Error: {e}")

    def _all_off(self):
        GPIO.output(self.PIN_GREEN, GPIO.LOW)
        GPIO.output(self.PIN_RED, GPIO.LOW)
        GPIO.output(self.PIN_YELLOW, GPIO.LOW)

    async def start_heartbeat(self):
        """
        Blinks the Yellow LED every 2 seconds to indicate the scheduler is alive.
        """
        self.running = True
        logger.info("Starting LED Heartbeat (Yellow)...")
        try:
            while self.running:
                GPIO.output(self.PIN_YELLOW, GPIO.HIGH)
                await asyncio.sleep(0.5)
                GPIO.output(self.PIN_YELLOW, GPIO.LOW)
                await asyncio.sleep(1.5)
        except asyncio.CancelledError:
            logger.info("Heartbeat task cancelled.")
            self._all_off()

    def stop(self):
        self.running = False
        self._all_off()
        GPIO.cleanup()

    def update_weather_status(self, db: Session):
        """
        Updates Green/Red LEDs based on the latest weather and dust data.
        
        Logic:
        - Optimal (Green): Sky Code <= 3 (Sunny/Cloudy) AND No Rain (PTY=0) AND Dust (PM10/PM2.5) is Good (Grade 1)
        - Bad (Red): Rain (PTY > 0) OR Dust is Bad (Grade >= 3)
        - Else: Both OFF (or could be another state, but user only specified Green/Red)
        """
        try:
            now = get_kst_now()
            date_str = now.strftime("%Y%m%d")
            time_str = now.strftime("%H00")
            
            # 1. Get Hourly Forecast (Sky, PTY)
            # Find the closest forecast for current time
            forecast = db.query(HourlyForecast).filter(
                HourlyForecast.base_date == date_str,
                HourlyForecast.base_time == time_str
            ).first()

            # 2. Get Dust Info
            # Find latest dust info (using today's date or most recent)
            # Note: Dust dataTime format is usually "YYYY-MM-DD HH:MM"
            # We'll just grab the latest entry for simplicity or filter by date if needed.
            # For now, let's try to find a record for today.
            dust_date_prefix = now.strftime("%Y-%m-%d")
            dust = db.query(Dust).filter(
                Dust.dataTime.like(f"{dust_date_prefix}%")
            ).order_by(Dust.dataTime.desc()).first()

            is_optimal = False
            is_bad = False

            # Default values if data missing
            sky = 0
            pty = 0
            pm10_grade = 1
            pm25_grade = 1

            if forecast:
                sky = forecast.sky_code or 0
                pty = forecast.precip_type or 0
            
            if dust:
                # Grade: 1(Good), 2(Normal), 3(Bad), 4(Very Bad)
                # API returns string "1", "2", etc.
                try:
                    pm10_grade = int(dust.pm10Grade) if dust.pm10Grade and dust.pm10Grade.isdigit() else 2
                    pm25_grade = int(dust.pm25Grade) if dust.pm25Grade and dust.pm25Grade.isdigit() else 2
                except:
                    pass

            # Logic Evaluation
            # Bad Condition
            if pty > 0 or pm10_grade >= 3 or pm25_grade >= 3:
                is_bad = True
            # Optimal Condition (Strict)
            elif sky <= 3 and pty == 0 and pm10_grade == 1 and pm25_grade == 1:
                is_optimal = True
            
            # Apply to LEDs
            if is_bad:
                GPIO.output(self.PIN_RED, GPIO.HIGH)
                GPIO.output(self.PIN_GREEN, GPIO.LOW)
                logger.info(f"Weather Status: BAD (PTY={pty}, Dust={pm10_grade}/{pm25_grade}) -> RED ON")
            elif is_optimal:
                GPIO.output(self.PIN_RED, GPIO.LOW)
                GPIO.output(self.PIN_GREEN, GPIO.HIGH)
                logger.info(f"Weather Status: OPTIMAL (Sky={sky}, Dust={pm10_grade}/{pm25_grade}) -> GREEN ON")
            else:
                # Neutral / Normal
                GPIO.output(self.PIN_RED, GPIO.LOW)
                GPIO.output(self.PIN_GREEN, GPIO.LOW)
                logger.info(f"Weather Status: NORMAL (Sky={sky}, Dust={pm10_grade}/{pm25_grade}) -> LEDs OFF")

        except Exception as e:
            logger.error(f"Error updating weather LED status: {e}")
