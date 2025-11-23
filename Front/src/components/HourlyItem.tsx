import React from 'react';
import WeatherIcon, { type WeatherConditionKey } from './WeatherIcon'; 

interface HourlyItemProps {
    time: string;
    icon: string; 
    temp: number;
}

const HourlyItem: React.FC<HourlyItemProps> = ({ time, icon, temp }) => {
    
    // === [설정] 아이콘별 크기 조정 맵 (컴포넌트 내부로 이동) ===
    // 경고를 없애기 위해 함수 안으로 정의를 옮겼습니다.
    const ICON_SIZE_MAP: Record<WeatherConditionKey, number> = {
        // 기본 크기 (45px)
        'sun': 80,
        'cloud_sun': 78,
        'cloud': 80,
        'rain': 60,
        'snow': 68,
        'sunrise_sunset': 77,
        'cloud_moon': 70, 

        // 달 아이콘 크기 (35px)
        'moon': 55
    
    };
    // ===========================================

    const condition = icon as WeatherConditionKey;

    // ICON_SIZE_MAP의 값을 여기서 읽어 currentSize를 결정합니다.
    const currentSize = ICON_SIZE_MAP[condition] || 45;

    return (
        // flex-col: 수직 정렬, gap-2: 요소 간 간격
        <div className="flex flex-col items-center justify-between gap-2 min-w-[60px]">
            
            {/* 1. 시간 텍스트 */}
            <span className="text-white/80 font-medium text-[35px] mb-1">
                {time}
            </span>

            {/* 2. 날씨 아이콘 */}
            {/* 템플릿 리터럴로 w-h 클래스에 currentSize 값을 적용 */}
            <div className={`py-1 w-[${currentSize}px] h-[${currentSize}px] flex items-center justify-center`}> 
                <WeatherIcon 
                    condition={condition} 
                    width={currentSize} 
                    height={currentSize}
                    className="drop-shadow-sm"
                />
            </div>

            {/* 3. 온도 텍스트 */}
            <span className="text-white font-bold text-[34px] mt-1">
                {temp}°
            </span>

        </div>
    );
};

export default HourlyItem;