import React, { useEffect, useState } from 'react';
import axios from 'axios';
import WeatherIcon, { type WeatherConditionKey } from './WeatherIcon';

// --- 설정 ---
const CONFIG = {
  gap: "gap-10",
  daySize: "text-[38px]",
  iconSize: 100,
  tempSize: "text-[42px]",
  barHeight: "h-[18px]",
  scaleMin: -15, // 겨울철이라 범위 조정
  scaleMax: 20,
  barMargin: "mx-[70px]",
};

interface WeeklyData {
  day: string;
  type: WeatherConditionKey;
  min: number;
  max: number;
}

// 날씨 문자열 -> 아이콘 키 매핑
const mapWeatherToIcon = (wf: string): WeatherConditionKey => {
  if (!wf) return 'sun';
  if (wf.includes('비') || wf.includes('소나기')) return 'rain';
  if (wf.includes('눈')) return 'snow';
  if (wf.includes('흐림')) return 'cloud';
  if (wf.includes('구름많음')) return 'cloud_sun';
  return 'sun'; // 맑음
};

// 오전/오후 날씨 중 더 '나쁜' 날씨(비/눈 > 흐림 > 구름 > 맑음)를 선택
const getRepresentativeIcon = (wfAm: string, wfPm: string): WeatherConditionKey => {
  const iconAm = mapWeatherToIcon(wfAm);
  const iconPm = mapWeatherToIcon(wfPm);

  const priority = { 'snow': 4, 'rain': 3, 'cloud': 2, 'cloud_sun': 1, 'sun': 0, 'moon': 0, 'cloud_moon': 1, 'sunrise_sunset': 0 };

  // @ts-ignore
  if ((priority[iconPm] || 0) >= (priority[iconAm] || 0)) return iconPm;
  return iconAm;
};

const getDayName = (dateStr: string): string => {
  const date = new Date(
    parseInt(dateStr.substring(0, 4)),
    parseInt(dateStr.substring(4, 6)) - 1,
    parseInt(dateStr.substring(6, 8))
  );
  const today = new Date();

  // 오늘 날짜 확인
  if (date.getDate() === today.getDate() && date.getMonth() === today.getMonth()) {
    return "Today";
  }
  return `${date.getMonth() + 1}.${date.getDate()}`;
};

export default function WeeklyForecastList() {
  const [weeklyData, setWeeklyData] = useState<WeeklyData[]>([]);

  useEffect(() => {
    const baseUrl = import.meta.env.VITE_APP_API_URL || 'http://localhost:8000';
    axios.get(`${baseUrl}/api/weather/weekly`)
      .then(response => {
        if (response.data) {
          // 오늘 포함 6일치 데이터 (Today + 5 days)
          const slicedData = response.data.slice(0, 6);

          // 1. 데이터 매핑 (일단 있는 그대로)
          let mapped: WeeklyData[] = slicedData.map((item: any) => ({
            day: getDayName(item.fcstDate),
            type: getRepresentativeIcon(item.wfAm, item.wfPm),
            min: item.taMin, // null일 수 있음
            max: item.taMax  // null일 수 있음
          }));

          // 2. 결측치 보간 (Interpolation)
          // 앞뒤 날짜의 평균값으로 채움. 만약 앞뒤도 없으면 0으로 처리.
          for (let i = 0; i < mapped.length; i++) {
            // 최저기온 보간
            if (mapped[i].min === null || mapped[i].min === undefined) {
              const prev = i > 0 ? mapped[i - 1].min : null;
              const next = i < mapped.length - 1 ? mapped[i + 1].min : null;

              if (prev !== null && next !== null) mapped[i].min = Math.round((prev + next) / 2);
              else if (prev !== null) mapped[i].min = prev;
              else if (next !== null) mapped[i].min = next;
              else mapped[i].min = 0; // 최악의 경우
            }

            // 최고기온 보간
            if (mapped[i].max === null || mapped[i].max === undefined) {
              const prev = i > 0 ? mapped[i - 1].max : null;
              const next = i < mapped.length - 1 ? mapped[i + 1].max : null;

              if (prev !== null && next !== null) mapped[i].max = Math.round((prev + next) / 2);
              else if (prev !== null) mapped[i].max = prev;
              else if (next !== null) mapped[i].max = next;
              else mapped[i].max = 0;
            }

            // 날씨 아이콘 보간 (없으면 이전 날짜 따라감, 첫날이면 맑음)
            if (!mapped[i].type || mapped[i].type === 'sun') { // 'sun'이 기본값이므로, 원본 데이터가 비어서 sun이 된 경우를 가정
              // 주의: getRepresentativeIcon에서 이미 기본값이 'sun'이므로, 
              // 원본 wfAm/wfPm이 null이어서 'sun'이 된 것인지 구분이 어려울 수 있음.
              // 하지만 여기서는 간단히 'sun'인 경우 혹시 모르니 이전 날짜를 참고할 수도 있지만,
              // 사용자 요청은 "NULL인 경우"이므로, 위 매핑 단계에서 null 체크를 더 엄밀히 하거나
              // 여기서 값이 튀는 것을 방지. 
              // 일단 온도가 핵심이므로 온도는 보간 완료.
              // 날씨 상태는 API가 보통 3일차부터는 오전/오후 다 주므로 크게 문제 없을 듯.
              // 만약 3일차 데이터가 아예 비어있다면(API 오류 등), 이전 날짜 복사
              if (slicedData[i].wfAm === null && slicedData[i].wfPm === null) {
                if (i > 0) mapped[i].type = mapped[i - 1].type;
              }
            }
          }

          setWeeklyData(mapped);
        }
      })
      .catch(err => console.error("Weekly API Error:", err));
  }, []);

  const calculateBarPosition = (min: number, max: number) => {
    const range = CONFIG.scaleMax - CONFIG.scaleMin;
    let left = ((min - CONFIG.scaleMin) / range) * 100;
    let width = ((max - min) / range) * 100;
    if (left < 0) left = 0;
    if (left + width > 100) width = 100 - left;
    return { left: `${left}%`, width: `${width}%` };
  };

  if (weeklyData.length === 0) return <div className="text-white">Loading...</div>;

  return (
    <div className={`flex flex-col w-full h-full justify-center px-2 ${CONFIG.gap}`}>
      {weeklyData.map((item, index) => {
        const { left, width } = calculateBarPosition(item.min, item.max);
        const isLast = index === weeklyData.length - 1;

        return (
          <div key={index} className={`flex items-center justify-between w-full pb-3 ${!isLast ? 'border-b border-white/10' : ''}`}>
            {/* 1. 요일 */}
            <span className={`text-white font-medium ${CONFIG.daySize} w-[140px] text-left`}>
              {item.day}
            </span>

            {/* 2. 아이콘 */}
            <div className="flex justify-center w-[70px]">
              <WeatherIcon
                condition={item.type}
                width={CONFIG.iconSize}
                height={CONFIG.iconSize}
                className="drop-shadow-sm"
              />
            </div>

            {/* 3. 최저 온도 */}
            <span className={`text-white/60 font-medium ${CONFIG.tempSize} w-[80px] text-right`}>
              {item.min}°
            </span>

            {/* 4. 온도 막대 */}
            <div className={`flex-1 ${CONFIG.barMargin} ${CONFIG.barHeight} bg-black/20 rounded-full relative overflow-hidden`}>
              <div
                className="absolute top-0 h-full bg-gradient-to-r from-blue-300 via-yellow-200 to-orange-300 rounded-full opacity-90"
                style={{ left, width }}
              />
            </div>

            {/* 5. 최고 온도 */}
            <span className={`text-white font-medium ${CONFIG.tempSize} w-[70px] text-right`}>
              {item.max}°
            </span>
          </div>
        );
      })}
    </div>
  );
}