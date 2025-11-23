import React, { useEffect, useState } from 'react';
import axios from 'axios';
import WeatherIcon, { type WeatherConditionKey } from './WeatherIcon';

// --- [Type Definition] (유지) ---
interface WeatherData {
    location: string;
    current_temp: number;
    high_temp: number;
    low_temp: number;
    timestamp: string;
    sky_value: string;
    pty_value: string;
}

// --- 헬퍼 함수들 (유지) ---
const isItNightTime = (timestamp: string): boolean => {
    if (!timestamp) return false;
    try {
        const hour = new Date(timestamp).getHours();
        return hour < 7 || hour > 19;
    } catch (e) {
        return false;
    }
};

const getThemeClassFromData = (sky: string, pty: string, timestamp: string): string => {
    const isNight = isItNightTime(timestamp);
    
    if (pty !== '없음') {
        if (pty === '눈' || pty === '눈/비') return 'theme-snowy';
        return isNight ? 'theme-night-rainy' : 'theme-rainy'; 
    }
    
    if (sky === '맑음') return isNight ? 'theme-night-clear' : 'theme-day-clear';
    if (sky === '흐림' || sky === '구름 많음') return isNight ? 'theme-night-cloudy' : 'theme-cloudy';
    
    return 'theme-day-clear';
};

const getIconConditionCode = (sky: string, pty: string, isNight: boolean): WeatherConditionKey => {
    if (pty !== '없음') {
        if (pty === '비' || pty === '소나기') return 'rain';
        if (pty === '눈' || pty === '눈/비') return 'snow';
    }
    if (isNight) {
        return sky === '맑음' ? 'moon' : 'cloud_moon'; // 밤에는 구름해 대신 구름달
    }
    return sky === '맑음' ? 'sun' : 'cloud';
};

// --- 비상용 가짜 데이터 (유지) ---
const DUMMY_DATA: WeatherData = {
    location: "광주광역시",
    current_temp: 12,
    high_temp: 15,
    low_temp: 1,
    timestamp: new Date().toISOString(),
    sky_value: "맑음", // 광선이 잘 보이도록 맑음으로 설정
    pty_value: "없음"
};


// --- 메인 컴포넌트 ---
const WeatherCurrent: React.FC = () => {
    // 로딩 및 API 로직 (유지)
    const [weatherData, setWeatherData] = useState<WeatherData>(DUMMY_DATA);
    
    useEffect(() => {
        const baseUrl = import.meta.env.VITE_APP_API_URL || 'http://localhost:8080'; 
        const apiUrl = `${baseUrl}/weather/current`;
        
        axios.get(apiUrl)
            .then(response => {
                if (response.data) {
                    setWeatherData(response.data); 
                    const themeClass = getThemeClassFromData(response.data.sky_value, response.data.pty_value, response.data.timestamp);
                    document.body.className = themeClass; 
                }
            })
            .catch((err) => {
                console.log("백엔드 연결 실패 (더미 데이터 사용):", err);
            });
    }, []); 

    // 로딩/에러 처리 (유지)
    // 이 부분은 간결하게 처리했습니다.
    if (!weatherData) return <div className="text-white text-center p-10">날씨 로딩 중... ⏳</div>;


    const { 
        location, 
        current_temp, high_temp, low_temp, timestamp, sky_value, pty_value
    } = weatherData;

    const isNight = isItNightTime(timestamp);
    const iconCondition = getIconConditionCode(sky_value, pty_value, isNight); 
    
    // --- 새로운 Sun SVG (현재 날씨 전용 - 배경 글로우) ---
    const SunGlowSVG = (
        <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 128 120" fill="none">
          <path d="M128 60C128 93.1371 99.3462 120 64 120C28.6538 120 0 93.1371 0 60C0 26.8629 28.6538 0 64 0C99.3462 0 128 26.8629 128 60Z" fill="url(#paint0_radial_66_92)" fillOpacity="0.8"/>
          <defs>
            <radialGradient id="paint0_radial_66_92" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(64 60) rotate(90) scale(83.5135 89.0811)">
              <stop stopColor="#FFD88B"/>
              <stop offset="1" stopColor="#FFA900"/>
            </radialGradient>
          </defs>
        </svg>
    );

    return (
        <div className="w-full flex flex-row items-center justify-start gap-20 p-4">
                
                {/* === 1. 메인 아이콘 영역 (왼쪽) === */}
                {/* w-[180px] h-[180px]와 같은 고정 크기 제거됨 (너비 복구) */}
                <div className="relative flex items-center justify-center"> 
                    
                    {/* 1-1. 글로우 효과 (광선) */}
                    {/* ... (광선 코드) ... */}
                    
                    {/* 1-2. 메인 아이콘 (겹침 문제 유발 요소 없음) */}
                    <div className="relative z-10">
                        <WeatherIcon 
                            condition={iconCondition} 
                            className="drop-shadow-2xl" 
                            width={300}   
                            height={200} 
                    />
                </div>
            </div>

            {/* === 2. 텍스트 정보 (오른쪽) === */}
            <div className="flex flex-col items-start text-white drop-shadow-lg">
                
                {/* 위치 */}
                <p className="text-[40px] font-medium pl-2 opacity-90 mb-[20px]">
                    {location}
                </p>
                
                {/* 현재 온도 */}
                <h1 className="text-[120px] font-bold leading-none -ml-2">
                    {current_temp}°
                </h1>
                
                {/* 최고/최저 온도 */}
                <p className="text-[39px] font-medium pl-2 opacity-90 mt-[30px]">
                    H: {high_temp}°  L: {low_temp}°
                </p>
            </div>
            
        </div>
    );
}

export default WeatherCurrent;