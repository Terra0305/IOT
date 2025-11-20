import WeatherIcon from './WeatherIcon';
import React from 'react';
import { CloudIcon } from '../assets/icons'; // 더미 아이콘 임포트

// Props: 시간, 아이콘, 온도 데이터를 받아옵니다.
function HourlyItem({ time, icon, temp }) {
  
return (
    // [수정] 최상위 컨테이너 클래스 연결
    <div className="hourly-item-container"> 
      
      {/* 1. 시간 표시 */}
      <div className="item-time-text">
        {time}
      </div>

      {/* 2. 날씨 아이콘 */}
      <div className="item-weather-icon">
        <WeatherIcon condition={icon} size={24} />
        {icon || <p>☁️</p>} 
      </div>
      
      {/* 3. 온도 표시 */}
      <div className="item-temp-text">
        {temp}°
      </div>
      
    </div>
  );
}

export default HourlyItem;