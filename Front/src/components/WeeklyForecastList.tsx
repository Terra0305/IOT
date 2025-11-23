import React from 'react';
import WeatherIcon, { type WeatherConditionKey } from './WeatherIcon'; // WeatherIcon 임포트

// --- 설정: 여기서 숫자만 바꾸면 디자인이 변합니다! ---
const CONFIG = {
  // 1. 디자인/크기 설정
  gap: "gap-10",             
  daySize: "text-[38px]",   
  iconSize: 100,             // [수정!] 픽셀 단위로 변경 (SVG 크기 전달)
  tempSize: "text-[42px]",  
  barHeight: "h-[18px]",     
  
  // 2. 온도 바 기준점 (범위 조절용)
  scaleMin: -5, 
  scaleMax: 25, 
  
  // 3. 바 양옆 여백 (공간 확보)
  barMargin: "mx-[70px]", 
};

// 데이터 (WeatherConditionKey 타입에 맞게 키 값으로 변경)
const WEEKLY_DATA: { day: string; type: WeatherConditionKey; min: number; max: number }[] = [
  { day: "Today", type: 'sun',        min: 1, max: 15 },
  { day: "Mon",   type: 'cloud_sun',  min: 2, max: 14 },
  { day: "Tue",   type: 'cloud',      min: 0, max: 13 },
  { day: "Wed",   type: 'rain',       min: 3, max: 12 },
  { day: "Thu",   type: 'snow',       min: 1, max: 15 },
  { day: "Fri",   type: 'moon',       min: 2, max: 16 },
];

export default function WeeklyForecastList() {
  
  // 온도 바 위치 계산 함수 (CONFIG 설정값 사용)
  const calculateBarPosition = (min: number, max: number) => {
    const range = CONFIG.scaleMax - CONFIG.scaleMin;
    
    let left = ((min - CONFIG.scaleMin) / range) * 100;
    let width = ((max - min) / range) * 100;
    
    if (left < 0) left = 0;
    if (left + width > 100) width = 100 - left;
    
    return { left: `${left}%`, width: `${width}%` };
  };

  return (
    <div className={`flex flex-col w-full h-full justify-center px-2 ${CONFIG.gap}`}>
      
      {WEEKLY_DATA.map((item, index) => {
        const { left, width } = calculateBarPosition(item.min, item.max);
        const isLast = index === WEEKLY_DATA.length - 1;

        return (
          <div key={index} 
               className={`flex items-center justify-between w-full pb-3 ${!isLast ? 'border-b border-white/10' : ''}`}>
            
            {/* 1. 요일 */}
            <span className={`text-white font-medium ${CONFIG.daySize} w-[140px] text-left`}>
              {item.day}
            </span>

            {/* 2. 아이콘 (SVG 아이콘으로 교체!) */}
            <div className="flex justify-center w-[70px]">
               <WeatherIcon
                    condition={item.type} // 키 값 전달
                    width={CONFIG.iconSize}
                    height={CONFIG.iconSize}
                    className="drop-shadow-sm"
                />
            </div>

            {/* 3. 최저 온도 */}
            <span className={`text-white/60 font-medium ${CONFIG.tempSize} w-[80px] text-right`}>
              {item.min}°
            </span>

            {/* 4. 온도 막대 */}
            <div className={`flex-1 ${CONFIG.barMargin} ${CONFIG.barHeight} bg-black/20 rounded-full relative overflow-hidden`}>
            <div 
                className="absolute top-0 h-full bg-gradient-to-r from-blue-300 via-yellow-200 to-orange-300 rounded-full opacity-90"
                style={{ left, width }} 
            />
            </div>

            {/* 5. 최고 온도 */}
            <span className={`text-white font-medium ${CONFIG.tempSize} w-[70px] text-right`}>
              {item.max}°
            </span>

          </div>
        );
      })}
    </div>
  );
}