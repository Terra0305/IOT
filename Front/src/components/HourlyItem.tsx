// src/components/HourlyItem.tsx

import React from 'react';
import WeatherIcon from './WeatherIcon';

// 1. [Type] Props가 어떤 데이터를 받는지 정의합니다.
interface HourlyItemProps {
    time: string;
    icon: string;
    temp: number;
}

const HourlyItem: React.FC<HourlyItemProps> = ({ time, icon, temp }) => {
  return (
    <div className="hourly-item-container"> 
      <div className="item-time-text">
        {time}
      </div>
      <div className="item-weather-icon">
        <WeatherIcon condition={icon} size={24} /> 
      </div>
      <div className="item-temp-text">
        {temp}°
      </div>
    </div>
  );
}

export default HourlyItem;