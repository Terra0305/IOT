// src/components/WeeklyForecastList.tsx

import React from 'react';
import WeeklyItem from './WeeklyItem.tsx'; // .tsx 확장자 명시

// 1. [Type Definition] 데이터의 형태를 정의합니다. (Error 7006 해결)
interface WeeklyData {
    day: string;
    icon: string;
    tempLow: number;
    tempHigh: number;
}

// 2. [Data] 주간 예보 더미 데이터 (타입 적용)
const DUMMY_WEEKLY_DATA: WeeklyData[] = [
    { day: 'today', icon: 'sun', tempLow: 1, tempHigh: 15 },
    { day: 'sun', icon: 'cloud_sun', tempLow: 3, tempHigh: 18 },
    { day: 'mon', icon: 'rain', tempLow: -1, tempHigh: 10 },
    { day: 'tue', icon: 'snow', tempLow: 5, tempHigh: 25 },
    { day: 'wed', icon: 'cloud', tempLow: 12, tempHigh: 22 },
    { day: 'thu', icon: 'rain', tempLow: 10, tempHigh: 28 },
    { day: 'fri', icon: 'sun', tempLow: 8, tempHigh: 20 },
];

const WeeklyForecastList: React.FC = () => {
    
    // 3. [Logic] 주간 전체의 최저/최고 온도 계산 (Error 2304 해결: 변수명 통일)
    // (weeklyData가 아니라 DUMMY_WEEKLY_DATA를 사용해야 합니다)
    const allLows = DUMMY_WEEKLY_DATA.map(item => item.tempLow);
    const allHighs = DUMMY_WEEKLY_DATA.map(item => item.tempHigh);
    
    const weeklyMin = Math.min(...allLows); 
    const weeklyMax = Math.max(...allHighs);

    return (
        <div className="weekly-list-container">
            <h2>주간 예보 (Weekly Forecast)</h2>
            
            {/* 4. [Render] 데이터 매핑 */}
            {DUMMY_WEEKLY_DATA.map((item, index) => (
                <WeeklyItem
                    key={index}
                    day={item.day}
                    icon={item.icon}
                    tempLow={item.tempLow}
                    tempHigh={item.tempHigh}
                    
                    // [Error 2739 해결]: 필수 Prop인 min/max를 전달합니다.
                    weeklyMin={weeklyMin} 
                    weeklyMax={weeklyMax}
                />
            ))}
        </div>
    );
};

export default WeeklyForecastList;