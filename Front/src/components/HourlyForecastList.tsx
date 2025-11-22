// src/components/HourlyForecastList.tsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import HourlyItem from './HourlyItem';

// 1. [Type] API에서 받아올 데이터의 모양을 정의합니다.
// (Error 2339 'never' 해결)
interface HourlyForecastData {
    time: string;
    icon_code: string;
    temperature: number;
}

const HourlyForecastList: React.FC = () => {
    
    // 2. [Type] useState에 제네릭(<Type>)을 사용하여 타입을 명시합니다.
    
    // 빈 배열([])이지만, 미래에 HourlyForecastData가 들어올 것임을 명시
    const [hourlyData, setHourlyData] = useState<HourlyForecastData[]>([]);
    
    const [isLoading, setIsLoading] = useState<boolean>(true);
    
    // 초기값은 null이지만, 나중에 string(에러메시지)이 들어올 수 있음을 명시
    // (Error 2345 해결)
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const apiUrl = `${import.meta.env.VITE_APP_API_URL}/weather/hourly`;
        
        axios.get(apiUrl)
            .then((response: any) => { // <--- [수정] response에 : any 타입 추가
                // API 응답 구조에 맞춰 데이터 설정
                setHourlyData(response.data.hourly_forecasts || []); 
                setIsLoading(false);
            })
            // catch 블록의 err도 함께 수정 (이전에 7006 오류가 났을 수 있음)
            .catch((err: any) => { 
                console.error("API Error:", err);
                setError("시간별 예보 정보를 불러오는 데 실패했습니다.");
                setIsLoading(false);
            });
    }, []);

    if (isLoading) {
        return <div className="hourly-loading">Loading...</div>; 
    }
    if (error) {
        return <div className="hourly-error">{error}</div>;
    }

    return (
        <div className="hourly-list-viewport">
            <div className="hourly-list-scrollable">
                {
                    hourlyData.map((item, index) => (
                        <HourlyItem 
                            key={index}
                            time={item.time} 
                            // API 데이터의 키값(icon_code)과 Props 이름(icon) 매칭
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