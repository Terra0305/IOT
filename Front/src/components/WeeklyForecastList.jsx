// src/components/WeeklyForecastList.jsx

import React from 'react';
import WeeklyItem from './WeeklyItem'; // 방금 만든 개별 항목 컴포넌트 임포트

// ----------------------------------------------------
// 주간 예보 더미 데이터 (7일치)
// ----------------------------------------------------
const DUMMY_WEEKLY_DATA = [
    { day: 'today', icon: 'sunny', tempLow: 1, tempHigh: 15 },
    { day: 'sun', icon: 'cloudy', tempLow: 3, tempHigh: 18 },
    { day: 'mon', icon: 'cloudy', tempLow: 4, tempHigh: 19 },
    { day: 'tue', icon: 'rainy', tempLow: 2, tempHigh: 8 },
    { day: 'wed', icon: 'rainy', tempLow: 0, tempHigh: 9 },
    { day: 'thu', icon: 'sunny', tempLow: 0, tempHigh: 13 },
    { day: 'fri', icon: 'sunny', tempLow: 5, tempHigh: 13 },
];

function WeeklyForecastList() {
    
    return (
        // Figma의 WeeklyListContainer에 대응하는 구조입니다.
        <div className="weekly-list-container">
            <h2>주간 예보 (Weekly Forecast)</h2>
            
            {
                // 데이터 반복 렌더링
                DUMMY_WEEKLY_DATA.map((item, index) => (
                    <WeeklyItem
                        key={index}
                        day={item.day}
                        icon={item.icon}
                        tempLow={item.tempLow}
                        tempHigh={item.tempHigh}
                    />
                ))
            }
        </div>
    );
}

export default WeeklyForecastList;