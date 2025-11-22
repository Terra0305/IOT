// src/components/WeatherCurrent.tsx

import React, { useEffect, useState } from 'react';
import axios from 'axios';

// [1] WeatherIcon 컴포넌트와 타입(WeatherConditionKey)을 함께 임포트합니다.
// (WeatherIcon.tsx에서 'export type WeatherConditionKey'가 되어 있어야 합니다.)
import WeatherIcon, { type WeatherConditionKey } from './WeatherIcon';
// ----------------------------------------------------
// [Type Definition] 데이터 타입 정의 (TypeScript 필수)
// ----------------------------------------------------
interface WeatherData {
    location: string;
    current_temp: number;
    high_temp: number;
    low_temp: number;
    timestamp: string;
    sky_value: string;
    pty_value: string;
}

// ----------------------------------------------------
// 1. 헬퍼 함수: 시간대 판단 (낮/밤)
// ----------------------------------------------------
const isItNightTime = (timestamp: string): boolean => {
    if (!timestamp) return false;
    try {
        const hour = new Date(timestamp).getHours();
        return hour < 7 || hour > 19; // 19시~7시를 밤으로 가정
    } catch (e) {
        return false;
    }
};

// ----------------------------------------------------
// 2. 헬퍼 함수: 날씨 데이터 -> CSS 테마 클래스 변환
// ----------------------------------------------------
const getThemeClassFromData = (sky: string, pty: string, timestamp: string): string => {
    const isNight = isItNightTime(timestamp);
    
    // 강수 형태 (PTY) 우선
    if (pty !== '없음') {
        if (pty === '눈' || pty === '눈/비') return 'theme-snowy';
        return isNight ? 'theme-night-rainy' : 'theme-rainy'; 
    }
    
    // 하늘 상태 (SKY)
    if (sky === '맑음') return isNight ? 'theme-night-clear' : 'theme-day-clear';
    if (sky === '흐림' || sky === '구름 많음') return isNight ? 'theme-night-cloudy' : 'theme-cloudy';
    
    return 'theme-day-clear'; // 기본값
};

// ----------------------------------------------------
// 3. 헬퍼 함수: 날씨 데이터 -> 아이콘 조건 키(String) 변환
// ----------------------------------------------------
// 반환 타입을 WeatherConditionKey로 명시하여 WeatherIcon 컴포넌트와 호환되게 합니다.
const getIconConditionCode = (sky: string, pty: string, isNight: boolean): WeatherConditionKey => {
    // 강수
    if (pty !== '없음') {
        if (pty === '비' || pty === '소나기') return 'rain';
        if (pty === '눈' || pty === '눈/비') return 'snow';
    }
    // 야간
    if (isNight) {
        // 'moon' 키가 WeatherIcon의 ICON_MAP에 있어야 합니다.
        // 밤에 구름이 끼면 'cloud_sun'을 쓰거나, 'cloudy_night'를 추가 정의해서 써야 합니다.
        // 여기서는 기존 로직대로 'cloud_sun'을 사용합니다.
        return sky === '맑음' ? 'moon' : 'cloud_sun'; 
    }
    // 주간
    return sky === '맑음' ? 'sun' : 'cloud';
};


// ----------------------------------------------------
// 메인 컴포넌트: WeatherCurrent
// ----------------------------------------------------
const WeatherCurrent: React.FC = () => {
    // 상태 관리 (제네릭을 사용하여 타입 명시)
    const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    
    // A. 컴포넌트 마운트 시 API 호출
    useEffect(() => {
        const apiUrl = `${import.meta.env.VITE_APP_API_URL}/weather/current`;
        
        axios.get(apiUrl)
            .then(response => {
                const data = response.data as WeatherData; // 데이터 타입 단언
                setWeatherData(data); 
                setIsLoading(false);
                
                // [테마 적용] API 데이터를 받자마자 배경 테마 변경
                const themeClass = getThemeClassFromData(data.sky_value, data.pty_value, data.timestamp);
                document.body.className = themeClass; 
            })
            .catch((err: any) => {
                console.error("API Error:", err);
                setError("날씨 정보를 불러오는 데 실패했습니다.");
                setIsLoading(false);
            });
    }, []); 

    // B. 로딩 및 에러 화면 처리
    if (isLoading) return <div className="loading-spinner">데이터 로드 중...</div>; 
    if (error) return <div className="error-message">{error}</div>;
    if (!weatherData) return null; // 데이터가 없을 경우 방어 코드

    // C. 데이터 분해 할당
    const { 
        location, 
        current_temp, high_temp, low_temp, timestamp, sky_value, pty_value
    } = weatherData;

    // D. 렌더링 변수 계산
    const isNight = isItNightTime(timestamp);
    const iconCondition = getIconConditionCode(sky_value, pty_value, isNight); 
    const glowClass = isNight ? 'moon-glow' : 'sun-glow'; // 배경 빛 효과 클래스

    return (
        <div className="weather-current-container">
            
            {/* 1. 텍스트 정보 (위치, 온도) */}
            <div className="weather-header-container">
                <p className="location-name">{location || '위치 정보 없음'}</p>
                <h1 className="current-temp">{current_temp}°</h1>
                <p className="temp-range">
                    H: {high_temp}° / L: {low_temp}°
                </p>
            </div>
            
            {/* 2. 메인 아이콘 영역 */}
            <div className="current-icon-area">
                
                {/* 2-1. 별 배경 (밤 맑음일 때만) */}
                {(isNight && sky_value === '맑음') && <div className="star-field-container" />}

                {/* 2-2. 글로우 효과 (CSS로 아이콘 뒤에 배치됨) */}
                <div className={glowClass} />

                {/* 2-3. 메인 아이콘 (WeatherIcon 컴포넌트 사용) */}
                <div className="current-icon-display">
                    <WeatherIcon 
                        condition={iconCondition} 
                        className="main-weather-icon" 
                        width={180}   
                        height={170}  
                    />
                </div>
                
                {/* 2-4. 모션 요소 (나비/Lottie 자리) */}
                 <div className="visual-enhancer-motion">
                    <p style={{ fontSize: '1rem' }}>🦋</p>
                </div>
            </div>
        </div>
    );
}

export default WeatherCurrent;