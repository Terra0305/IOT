// src/components/HourlyForecastList.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import HourlyItem from './HourlyItem'; // 방금 만든 개별 항목 컴포넌트 임포트

function HourlyForecastList() {
    
    // 1. API 응답 상태 및 로딩 상태 정의
    const [hourlyData, setHourlyData] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    // 2. 컴포넌트 마운트 시 API 호출 (시간별 예보 데이터)
    useEffect(() => {
        const apiUrl = `${import.meta.env.VITE_APP_API_URL}/weather/hourly`;
        
        axios.get(apiUrl)
            .then(response => {
                // API 응답 구조에 따라 데이터 배열을 설정합니다.
                // (예시: API가 hourly_forecasts라는 배열을 반환한다고 가정)
                setHourlyData(response.data.hourly_forecasts || []); 
                setIsLoading(false);
            })
            .catch(err => {
                console.error("API Error fetching hourly weather:", err);
                setError("시간별 예보 정보를 불러오는 데 실패했습니다.");
                setIsLoading(false);
            });
    }, []);

    // 3. 로딩 및 에러 처리 UI
    if (isLoading) {
        return <div className="hourly-loading">시간별 예보 로드 중...</div>; 
    }
    if (error) {
        return <div className="hourly-error">{error}</div>;
    }

    return (
        // [수정] Outer Frame (Viewport) 클래스 연결
        <div className="hourly-list-viewport">
            {/* [수정] Inner Frame (Scrollable List) 클래스 연결 */}
            <div className="hourly-list-scrollable">
                {
                    hourlyData.map((item, index) => (
                        <HourlyItem 
                            key={index}
                            time={item.time} 
                            icon={item.icon_code} 
                            temp={item.temperature} 
                        />
                    ))
                }
            </div>
        </div>
    );
}

export default HourlyForecastList;