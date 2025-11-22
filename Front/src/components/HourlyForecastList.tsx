// src/components/HourlyForecastList.tsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import HourlyItem from './HourlyItem';

interface HourlyForecastData {
    time: string;
    icon_code: string;
    temperature: number;
}

// --- [추가] UI 테스트용 더미 데이터 ---
const MOCK_HOURLY_DATA: HourlyForecastData[] = [
    { time: "Now", icon_code: "sun", temperature: 14 },
    { time: "1pm", icon_code: "sun", temperature: 15 },
    { time: "2pm", icon_code: "cloud_sun", temperature: 16 },
    { time: "3pm", icon_code: "cloud", temperature: 16 },
    { time: "4pm", icon_code: "rain", temperature: 15 },
    { time: "5pm", icon_code: "rain", temperature: 14 },
    { time: "6pm", icon_code: "cloud", temperature: 13 },
    { time: "7pm", icon_code: "moon", temperature: 12 },
    { time: "8pm", icon_code: "moon", temperature: 11 },
    { time: "9pm", icon_code: "cloud", temperature: 10 },
    { time: "10pm", icon_code: "cloud", temperature: 9 },
    { time: "11pm", icon_code: "moon", temperature: 8 },
    // ... 필요하면 더 추가
];

const HourlyForecastList: React.FC = () => {
    
    const [hourlyData, setHourlyData] = useState<HourlyForecastData[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const apiUrl = `${import.meta.env.VITE_APP_API_URL}/weather/hourly`;
        
        // --- [수정] API 호출 대신 더미 데이터 사용 ---
        // 백엔드 연결 전까지는 이 부분이 UI를 보여줍니다.
        
        // 1. (나중에 쓸 코드) 실제 API 호출은 주석 처리
        /*
        axios.get(apiUrl)
            .then((response: any) => {
                setHourlyData(response.data.hourly_forecasts || []); 
                setIsLoading(false);
            })
            .catch((err: any) => { 
                console.error("API Error:", err);
                // 에러가 나더라도 UI를 보기 위해 더미 데이터 설정 (임시)
                setHourlyData(MOCK_HOURLY_DATA); 
                setIsLoading(false);
            });
        */

        // 2. (현재 쓸 코드) 더미 데이터 즉시 로드
        setTimeout(() => {
            setHourlyData(MOCK_HOURLY_DATA);
            setIsLoading(false);
        }, 500); // 0.5초 뒤에 로딩 끝

    }, []);

    // 로딩 중일 때 표시
    if (isLoading) {
        return <div className="hourly-loading">Loading...</div>; 
    }
    
    // 에러가 있어도 데이터를 보여주도록 로직 변경 (더미 데이터 사용 시 에러 화면 안 보임)
    if (error && hourlyData.length === 0) {
        return <div className="hourly-error">{error}</div>;
    }

    return (
        // Tailwind CSS 클래스 유지 + 기존 CSS 클래스(hourly-list-scrollable) 호환
        <div className="hourly-list-viewport w-full overflow-x-auto no-scrollbar py-3">
            <div className="hourly-list-scrollable flex gap-4 px-2 min-w-max">
                {hourlyData.map((item, index) => (
                    <HourlyItem
                        key={index}
                        time={item.time}
                        icon={item.icon_code}
                        temp={item.temperature}
                    />
                ))}
            </div>
        </div>
    );
}

export default HourlyForecastList;