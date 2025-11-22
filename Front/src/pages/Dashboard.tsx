import SummaryResultCard from '../components/SummaryResultCard';
import DetailCardsGrid from '../components/DetailCardsGrid';
import WeeklyForecastList from '../components/WeeklyForecastList';
import HourlyForecastList from '../components/HourlyForecastList';
import WeatherCurrent from '../components/WeatherCurrent';
import React from 'react';

const DUMMY_LOCATION = "광주광역시";
const DUMMY_TEMP = 12;
const DUMMY_TEMP_HIGH = 15;
const DUMMY_TEMP_LOW = 1;

export default function Dashboard() {
  return (
    <div className="w-full max-w-screen-xl mx-auto px-4 py-6 flex flex-col gap-8">

      {/* ====================== */}
      {/* 1) 현재 날씨 메인 헤더 */}
      {/* ====================== */}
      <div className="flex flex-col items-center text-center gap-2">
        <p className="text-lg font-medium">{DUMMY_LOCATION}</p>
        <h1 className="text-6xl font-bold">{DUMMY_TEMP}°</h1>
        <p className="text-sm opacity-70">H: {DUMMY_TEMP_HIGH}  L: {DUMMY_TEMP_LOW}</p>

        {/* WeatherCurrent 아이콘 영역 */}
        <div className="mt-4">
          <WeatherCurrent />
        </div>
      </div>

      {/* ====================== */}
      {/* 2) 시간별 예보 (가로 스크롤) */}
      {/* ====================== */}
      <div className="w-full">
        <HourlyForecastList />
      </div>

      {/* ====================================== */}
      {/* 3) 주간 예보 + 상세 카드 + 종합 결과 */}
      {/* ====================================== */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        {/* -------- 좌측: 주간 예보 -------- */}
        <div className="md:col-span-1">
          <WeeklyForecastList />
        </div>

        {/* -------- 우측: 상세 + 종합 결과 -------- */}
        <div className="md:col-span-2 flex flex-col gap-6">

          {/* 상세 카드 4개 */}
          <DetailCardsGrid />

          {/* 종합 결과 카드 */}
          <SummaryResultCard />
        </div>

      </div>

    </div>
  );
}
