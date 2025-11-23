// src/components/WeeklyItem.tsx (전체 코드)

import React from 'react';
import WeatherIcon from './WeatherIcon';

// 1. [TypeScript] Props 타입 정의 (Error 7031 해결)
// 부모에게서 받아올 데이터의 "형태"를 미리 정의합니다.
interface WeeklyItemProps {
    day: string;       // 예: 'mon', 'tue'
    icon: string;      // 예: 'sun', 'rain'
    tempLow: number;   // 예: 5
    tempHigh: number;  // 예: 15
    weeklyMin: number; // 주간 최저 (계산용)
    weeklyMax: number; // 주간 최고 (계산용)
}

// 2. [TypeScript] 컴포넌트에 타입 적용 (React.FC<WeeklyItemProps>)
const WeeklyItem: React.FC<WeeklyItemProps> = ({ day, icon, tempLow, tempHigh, weeklyMin, weeklyMax }) => {
    
    // 3. [Logic Fix] 막대 바 길이 및 위치 계산 (변수 중복 선언 해결)
    // (이전 코드에서 중복 선언되었던 부분을 하나로 통합했습니다.)
    
    const range = weeklyMax - weeklyMin; 
    const barLength = tempHigh - tempLow; 
    const barOffset = tempLow - weeklyMin; 
    
    // 0으로 나누기 방지 (안전장치)
    const validRange = range > 0 ? range : 1; 

    // 백분율 계산
    const widthPercent = (barLength / validRange) * 100;
    const offsetPercent = (barOffset / validRange) * 100;

    return (
        <div className="weekly-item-container"> 
            
            {/* 1. 요일 텍스트 */}
            <div className="day-of-week-text">
                {day} 
            </div>

            {/* 2. 날씨 아이콘 */}
            <div className="weekly-weather-icon">
                <WeatherIcon condition={icon} size={40} />
            </div>
            
            {/* 3. 온도 요약 및 막대 바 그룹 */}
            <div className="temp-bar-group">
                
                {/* 3-1. 최저 온도 */}
                <div className="temp-low-value">{tempLow}°</div>

                {/* 3-2. 온도 막대 트랙 */}
                <div className="temp-scale-track">
                    {/* 3-3. 실제 온도 범위 채우기 (동적 스타일 적용) */}
                    <div 
                        className="temp-range-fill" 
                        style={{ 
                            width: `${widthPercent}%`, 
                            left: `${offsetPercent}%` // marginLeft 대신 left 사용 (position: absolute이므로)
                        }} 
                    > 
                    </div>
                </div>

                {/* 3-4. 최고 온도 */}
                <div className="temp-high-value">{tempHigh}°</div>
            </div> 
            
        </div>
    );
};

export default WeeklyItem;