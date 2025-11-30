import { useEffect, useState } from 'react';
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

// --- 아이콘 결정 로직 (Day/Night + Sky + PTY) ---
const getIconCode = (pty: number, sky: number, timeStr: string): string => {
    // 1. 시간 파싱 (HH:MM -> HH)
    const hour = parseInt(timeStr.split(':')[0], 10);
    // [수정] 겨울철 일출 시간을 고려하여 07시 이전은 밤으로 처리 (기존 06시 -> 07시)
    const isNight = hour < 7 || hour >= 18;

    // 2. 강수 형태 (PTY) 우선 처리
    if (pty > 0) {
        if (pty === 1 || pty === 4) return "rain"; // 비, 소나기
        if (pty === 2 || pty === 3) return "snow"; // 비/눈, 눈
    }

    // 3. 하늘 상태 (SKY) 처리
    // SKY: 1(맑음), 3(구름많음), 4(흐림)
    if (sky === 1) {
        return isNight ? "moon" : "sun";
    }
    if (sky === 3) {
        return isNight ? "cloud_moon" : "cloud_sun";
    }

    // sky === 4 (흐림) -> 구름 아이콘
    return "cloud";
};

export default function HourlyForecastList() {
    // [수정!] 초기값은 DUMMY_HOURLY_DATA로 설정합니다.
    const [hourlyData, setHourlyData] = useState<HourlyData[]>(DUMMY_HOURLY_DATA);

    // API 호출 로직 (Daily Forecast API 호출)
    useEffect(() => {
        const baseUrl = import.meta.env.VITE_APP_API_URL ?? 'http://localhost:8000';
        // 백엔드의 24시간 예보 API 주소 (Daily)
        const apiUrl = `${baseUrl}/api/weather/daily`;

        axios.get(apiUrl)
            .then(response => {
                // API에서 24시간 데이터를 성공적으로 받아오면 업데이트합니다.
                if (response.data && response.data.length > 0) {
                    // 데이터 구조가 다르다면 여기에 매핑 로직을 추가해야 합니다.
                    // 1. 현재 시간 (시간 단위) 구하기
                    const now = new Date();
                    const currentHour = now.getHours();
                    const currentDateStr = now.toISOString().slice(0, 10).replace(/-/g, ""); // YYYYMMDD

                    // 2. 전체 데이터 중 현재 시간 이후의 데이터만 필터링
                    // (날짜가 오늘이고 시간이 현재시간 이상이거나, 날짜가 미래인 경우)
                    const futureData = response.data.filter((item: any) => {
                        const itemDate = item.base_date;
                        const itemHour = parseInt(item.base_time.substring(0, 2), 10);

                        if (itemDate > currentDateStr) return true;
                        if (itemDate === currentDateStr && itemHour >= currentHour) return true;
                        return false;
                    });

                    // 3. 24개만 자르기
                    const next24Hours = futureData.slice(0, 24);

                    // 4. 데이터 매핑 및 시간 포맷팅 (12시간제)
                    const mappedData: HourlyData[] = next24Hours.map((item: any) => {
                        const timeStr = item.base_time.substring(0, 2) + ":00";
                        const hour24 = parseInt(item.base_time.substring(0, 2), 10);

                        // 12시간제 변환
                        let displayTime;
                        if (hour24 === 0) displayTime = "12 AM";
                        else if (hour24 === 12) displayTime = "12 PM";
                        else if (hour24 > 12) displayTime = `${hour24 - 12} PM`;
                        else displayTime = `${hour24} AM`;

                        // "Now" 처리 (첫 번째 항목이 현재 시간과 같으면)
                        // 하지만 사용자 요청은 "12 AMPM 형식"이므로 일단 포맷대로 표시하되, 
                        // 필요하면 첫 번째를 "Now"로 할 수도 있음. 여기서는 요청대로 포맷팅만 적용.

                        return {
                            time: displayTime,
                            temperature: item.temperature,
                            icon_code: getIconCode(item.precip_type, item.sky_code || 1, timeStr)
                        };
                    });
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