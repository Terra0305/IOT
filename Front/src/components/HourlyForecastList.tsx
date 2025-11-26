import React, { useEffect, useState } from 'react';
import axios from 'axios';
import HourlyItem from './HourlyItem';

// --- [Type Definition] 시간별 데이터 타입 ---
interface HourlyData {
    time: string; // 예: "12:00"
    temperature: number; // T1H
    icon_code: string; // WeatherConditionKey에 해당하는 값 (예: "sun", "cloud")
}

// --- 임시 더미 데이터 (24시간 분량으로 확장) ---
const createDummyData = (): HourlyData[] => {
    const data: HourlyData[] = [];
    const now = new Date();
    
    // 아이콘 목록 (반복 사용)
    const icons = ["sun", "cloud_sun", "cloud", "rain", "snow", "moon", "cloud_moon", "sunrise_sunset"];
    
    for (let i = 0; i < 24; i++) {
        const hour = now.getHours() + i;
        const displayHour = hour % 12 || 12; // 12시간제로 표시
        const ampm = hour % 24 < 12 ? 'am' : 'pm';
        
        data.push({
            time: i === 0 ? "Now" : `${displayHour}${ampm}`,
            icon_code: icons[i % icons.length],
            temperature: 10 + Math.floor(Math.sin(i / 4) * 5) // 임시 온도 변화
        });
    }
    return data;
};

const DUMMY_HOURLY_DATA: HourlyData[] = createDummyData();

const getIconCode = (pty: number, sky: number): string => {
    if (pty > 0) {
        if (pty === 1 || pty === 4) return "rain";
        if (pty === 2 || pty === 3) return "snow";
    }
    if (sky === 1) return "sun";
    if (sky === 3) return "cloud_sun";
    return "cloud";
};


export default function HourlyForecastList() {
    // [수정!] 초기값은 DUMMY_HOURLY_DATA로 설정합니다.
    const [hourlyData, setHourlyData] = useState<HourlyData[]>(DUMMY_HOURLY_DATA);
    
    // API 호출 로직 (Daily Forecast API 호출)
    useEffect(() => {
        const baseUrl = import.meta.env.VITE_APP_API_URL || 'http://localhost:8000';
        // 백엔드의 24시간 예보 API 주소 (Daily)
        const apiUrl = `${baseUrl}/api/weather/daily`; 

        axios.get(apiUrl)
            .then(response => {
                // API에서 24시간 데이터를 성공적으로 받아오면 업데이트합니다.
                if (response.data && response.data.length > 0) {
                    // 데이터 구조가 다르다면 여기에 매핑 로직을 추가해야 합니다.
                    const mappedData: HourlyData[] = response.data.map((item: any) => ({
                        time: item.base_time.substring(0, 2) + ":00", // "1200" -> "12:00"
                        temperature: item.temperature,
                        icon_code: getIconCode(item.precip_type, item.sky_code) // Helper needed
                    }));
                    setHourlyData(mappedData); 
                }
            })
            .catch(err => {
                // 실패해도 더미 데이터는 유지됩니다.
                console.warn("24시간 예보 API 연결 실패. 더미 데이터를 사용합니다.", err);
            });
    }, []);

    return (
        // Tailwind CSS 클래스 유지
        <div className="hourly-list-viewport w-full overflow-x-auto no-scrollbar py-3">
            {/* gap-[70px]: 요소 간 간격, min-w-max: 가로 스크롤 허용 */}
            <div className="hourly-list-scrollable flex gap-[79px] px-2 min-w-max">
                {hourlyData.map((item, index) => (
                    <HourlyItem
                        key={index}
                        time={item.time}
                        icon={item.icon_code} // 이 이름으로 HourlyItem에 전달
                        temp={item.temperature}
                    />
                ))}
            </div>
        </div>
    );
}