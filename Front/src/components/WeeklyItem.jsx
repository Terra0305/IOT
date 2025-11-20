
import React from 'react';
import WeatherIcon from './WeatherIcon'; 


function WeeklyItem({ day, icon, tempLow, tempHigh }) {
    
const barOffset = tempLow - weeklyMin; // 당일 최저 온도가 주간 최저 온도보다 얼마나 높은가
// ...
const offsetPercent = (barOffset / range) * 100; // 왼쪽 여백 (marginLeft)으로 사용

    return (
        <div className="weekly-item-container"> 
            
            {/* 1. 요일 텍스트 */}
            <div className="day-of-week-text">
                {day} 
            </div>

            {/* 2. 날씨 아이콘 */}
            <div className="weekly-weather-icon">
                {/* [수정] WeatherIcon 컴포넌트 사용을 위해 임시로 SunIcon/CloudIcon 대신 WeatherIcon으로 변경 */}
                <WeatherIcon condition={icon} size={24} />
            </div>
            
            {/* 3. 온도 요약 및 막대 바 그룹 (가로 Flex Container) */}
            <div className="temp-bar-group">
                
                {/* 3-1. 최저 온도 텍스트 (Left Fixed) */}
                <div className="temp-low-value">{tempLow}°</div>

                {/* 3-2. 온도 막대 트랙 (Parent: position: relative) */}
                <div className="temp-scale-track">
                    {/* 3-3. 실제 온도 범위 채우기 (Child: position: absolute) */}
                    {/* [수정] style 속성 대신 className을 사용하며, width/left는 JS로 처리됩니다. */}
                    <div 
                        className="temp-range-fill" 
                        style={{
                            width: `${widthPercent}%`, // 바의 길이
                            marginLeft: `${offsetPercent}%`, // 바의 시작 위치 (앞/뒤 이동)
                        }}>
                    </div>
                </div> {/* <-- [수정] temp-scale-track 닫는 태그 추가 */}

                {/* 3-4. 최고 온도 텍스트 (Right Fixed) */}
                <div className="temp-high-value">{tempHigh}°</div>
            </div> 
            
        </div>
    );
}

export default WeeklyItem;