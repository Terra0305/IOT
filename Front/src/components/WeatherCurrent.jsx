// src/components/WeatherCurrent.jsx (전체 코드)

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { SunIcon, MoonIcon } from '../assets/icons'; // 가상의 아이콘 파일 임포트
import { RainIcon, SnowIcon, CloudIcon, MoonCloudyIcon } from '../assets/icons'; // 기타 아이콘 임포트

// ----------------------------------------------------
// [컴포넌트 밖] 날씨 코드에 따른 아이콘 매핑 함수
// ----------------------------------------------------

{/* 2-3. 메인 아이콘 렌더링 */}
<IconComponent 
    className="main-weather-icon" 
    width={180}   // <--- 크기를 180px로 통일
    height={170}  // <--- 비율에 맞춰 높이를 170px로 통일 (예시 값)
/>

const getWeatherIcon = (sky, pty, isNight) => {
    // 1. 강수 형태 (PTY) 우선 순위
    if (pty === '비' || pty === '소나기') return RainIcon;
    if (pty === '눈' || pty === '눈/비') return SnowIcon;

    // 2. 야간 (Night) 하늘 상태 처리
    if (isNight) {
        if (sky === '맑음') return MoonIcon;
        return MoonCloudyIcon; // 밤 구름
    }
    
    // 3. 주간 (Day) 하늘 상태 처리
    if (sky === '맑음') return SunIcon;
    return CloudIcon; // 낮 구름

    if (isNight && sky === '맑음') return MoonIcon; 
    // ... 
    return SunIcon;

    
};

// 시간대 판단 함수
const isItNightTime = (timestamp) => {
    if (!timestamp) return false;
    try {
        const hour = new Date(timestamp).getHours();
        return hour < 7 || hour > 19; // 19시 이후 ~ 7시 이전은 밤으로 가정
    } catch (e) {
        return false;
    }
};

const getThemeClassFromData = (sky, pty, timestamp) => {
    
    const isNight = isItNightTime(timestamp); // 낮/밤 판단 로직

    // 1. 강수 형태 (PTY) 우선 순위
    if (pty === '비' || pty === '소나기') {
        // [수정] 밤이면 'theme-night-rainy', 낮이면 'theme-rainy' 사용
        return isNight ? 'theme-night-rainy' : 'theme-rainy'; 
    }
    
if (pty === '눈' || pty === '눈/비') {
        // [수정] 눈이 오면 낮/밤 관계없이 snow theme 사용
        return 'theme-snowy'; 
    }

    // 2. 하늘 상태 (SKY)
    if (sky === '흐림' || sky === '구름 많음') {
        return isNight ? 'theme-night-cloudy' : 'theme-cloudy';
    }
    
    // 3. 맑음 (기본값)
    return isNight ? 'theme-night-clear' : 'theme-day-clear';
};


function WeatherCurrent() {
    // API 응답을 저장할 상태 정의
    const [weatherData, setWeatherData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    
    // API 통신 로직 (생략 없이 유지)
    useEffect(() => {
        const apiUrl = `${import.meta.env.VITE_APP_API_URL}/weather/current`;
        
        axios.get(apiUrl)
            .then(response => {
                const data = response.data;
                setWeatherData(data); 
                setIsLoading(false);
                
                // 테마 클래스 설정
                const themeClass = getThemeClassFromData(data.sky_value, data.pty_value, data.timestamp);
                document.body.className = themeClass; // body에 직접 CSS 클래스 적용

            })
            .catch(err => {
                console.error("API Error fetching current weather:", err);
                setError("날씨 정보를 불러오는 데 실패했습니다.");
                setIsLoading(false);
            });
    }, []); 

    // 2. 로딩 및 에러 처리 (JSX)
    if (isLoading) {
        return <div className="loading-spinner">데이터 로드 중...</div>; 
    }
    if (error) {
        return <div className="error-message">{error}</div>;
    }
    
    // 3. API 데이터 구조 분해 및 아이콘 결정
    const { 
        location, 
        current_temp, high_temp, low_temp, timestamp, sky_value, pty_value
    } = weatherData || {};

    const isNight = isItNightTime(timestamp);
    const IconComponent = getWeatherIcon(sky_value, pty_value, isNight);
    const CurrentIconComponent = getWeatherIcon(sky_value, pty_value, isNight); // 표시할 아이콘 컴포넌트
    const glowClass = isNight ? 'moon-glow' : 'sun-glow'; // 글로우 CSS 클래스

    return (
        <div className="weather-current-container">
            
            {/* 1. 날씨 정보 헤더 (위치, 온도 등) */}
            <div className="weather-header-container">
                <p className="location-name">{location || '위치 정보'}</p>
                <h1 className="current-temp">{current_temp}°</h1>
                <p className="temp-range">
                    H: {high_temp}° / L: {low_temp}°
                </p>
            </div>
            
            {/* 2. 메인 아이콘 및 애니메이션 영역 (여기가 핵심) */}
            <div className="current-icon-area">
                
                {/* 2-1. 별 영역 (Night Clear에서만 조건부 렌더링) */}
                {(isNight && sky_value === '맑음') && <div className="star-field-container" />}

                {/* 2-2. 글로우 효과 (CSS에서 position: absolute로 아이콘 뒤에 깔림) */}
                <div className={glowClass} />

                {/* 2-3. 메인 아이콘 렌더링 (통일된 크기 prop 전달) */}
                <CurrentIconComponent 
                    className="main-weather-icon" 
                    width={180}   // 표준 너비
                    height={170}  // 표준 높이
                />

                {/* 2-4. Lottie 애니메이션/움직이는 요소 (🦋 자리) */}
                 <div className="visual-enhancer-motion">
                    <p style={{ fontSize: '1rem' }}>🦋</p>
                </div>
            </div>
            
        </div>
    );
}

function WeatherCurrent() {
    // ... (기존 로딩, 에러, 데이터 추출 로직) ...

    const { 
        location, 
        current_temp, high_temp, low_temp, timestamp, sky_value, pty_value
    } = weatherData || {};

    const isNight = isItNightTime(timestamp);
    const IconComponent = getWeatherIcon(sky_value, pty_value, isNight); // <-- MoonCloudyIcon이 여기서 결정됨
    
    const glowClass = (isNight && sky_value === '맑음') ? 'moon-glow' : ((isNight && sky_value !== '맑음') ? 'moon-cloudy-glow' : 'sun-glow'); // 글로우 클래스 업데이트
    
    // 1. 현재 body에 적용된 테마 클래스를 가져옵니다.
    const currentTheme = document.body.className;
    
    // 2. 현재 테마에 해당하는 Lottie 컴포넌트 선택
    const LottieComponent = MOTION_MAP[currentTheme];

    return (
        <div className="weather-current-container">
            {/* ... (기존 헤더 섹션) ... */}
            
            <div className="current-icon-area">
                
                {/* 별 또는 움직이는 요소 (Night Clear에서만) */}
                {(isNight && sky_value === '맑음') && <div className="star-field-container" />}
                
                {/* 글로우 효과 */}
                <div className={glowClass} />

                {/* 메인 아이콘 렌더링 */}
                <IconComponent className="main-weather-icon" width={247} height={238} />
                
                {/* [추가] 밤 흐림일 때 달 아이콘 위에 구름 아이콘 겹치기 */}
                {(isNight && (sky_value === '흐림' || sky_value === '구름 많음')) && (
                    <CloudIcon className="overlay-cloud-icon" size={150} color="white" 
                        style={{ position: 'absolute', top: '100px', left: '100px', zIndex: 2 }} 
                    /> // 위치와 크기 조정 필요
                )}

                <div className="visual-enhancer-motion">
                    <p style={{ fontSize: '1rem' }}>🦋</p>
                </div>
            </div>
            {/* 3. Lottie/모션 요소 자리 */}
            <div className="visual-enhancer-motion">
                {/* LottieComponent가 존재할 때만 렌더링 */}
                {LottieComponent && <LottieComponent className="lottie-visual" />}
                {/* <p>🦋</p> 코드를 LottieComponent로 대체 */}
            </div>
            
        </div>

        
    );
}

const MOTION_MAP = {
    // 배경 테마 클래스 : 렌더링할 Lottie 컴포넌트
    'theme-day-clear': ButterflyLottie,     // 맑은 날: 나비나 새
    'theme-day-cloudy': CloudMoveLottie,        // 흐린 날: 느린 구름 이동
    'theme-rainy': RainDropsLottie,         // 비 오는 날: 빗방울 효과
    'theme-night-clear': StarTwinkleLottie, // 맑은 밤: 별 반짝임
    'theme-night-cloudy': CloudMoveLottie,        // 흐린 날: 느린 구름 이동
    'theme-night-rainy': WindowFogLottie,   // 비 오는 밤: 창문 습기 효과
    'theme-snow': SnowMoveLottie,   // 눈 오는 날: 눈 내리는 효과
};

export default WeatherCurrent;