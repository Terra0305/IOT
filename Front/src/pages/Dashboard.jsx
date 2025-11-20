// src/pages/Dashboard.jsx (수정된 최종 구조)

import SummaryResultCard from '../components/SummaryResultCard';
import DetailCardsGrid from '../components/DetailCardsGrid';
import WeeklyForecastList from '../components/WeeklyForecastList';
import HourlyForecastList from '../components/HourlyForecastList';
import React from 'react';
import WeatherCurrent from '../components/WeatherCurrent'; // 현재 날씨 아이콘 영역
// WeatherHistory는 사용자 요청에 따라 제거됨

// ----------------------------------------------------
// (가정) Figma 디자인에서 결정된 날씨 정보 및 위치
// ----------------------------------------------------
const DUMMY_LOCATION = "광주광역시";
const DUMMY_TEMP = 12;
const DUMMY_TEMP_HIGH = 15;
const DUMMY_TEMP_LOW = 1;

function Dashboard() {
  
  return (
    // 'dashboard-container'는 전체 화면 레이아웃을 담당합니다.
    <div className="dashboard-container">
      
      {/* 1. 상단 현재 날씨 및 온도 요약 (Figma 상단) */}
      <div className="current-summary-block">
        
        {/* Figma에서 설계한 '광주광역시 12도 H:15 L:1' 영역 */}
        <div className="location-temp-group">
          <p className="location-text">{DUMMY_LOCATION}</p>
          <h1 className="current-temp-value">{DUMMY_TEMP}°</h1>
          <p className="high-low-temp-text">H: {DUMMY_TEMP_HIGH} L: {DUMMY_TEMP_LOW}</p>
        </div>
        
        {/* Figma 상단의 해/달 아이콘 및 빛 효과, 애니메이션 영역 */}
        <div className="main-icon-area">
          <WeatherCurrent /> {/* API 통신 결과로 아이콘/상태 표시 */}
          {/* Lottie_MotionElement 영역이 WeatherCurrent 내부에 포함되거나 별도 컴포넌트로 분리될 예정 */}
        </div>

      </div>
      
      {/* 2. 주요 정보 섹션 */}
      <div className="main-content-area">
          
          {/* 2-1. 시간별 예보 (Hourly Forecast Block) - 가로 스크롤, Full Width */}
          <div className="hourly-forecast-block">
              {/* HourlyScrollList 컴포넌트가 들어갈 영역 */}
              <HourlyForecastList />
          </div>
          
          {/* 2-2. 주간 예보 (좌) 및 상세 카드/종합 결과 (우) Grid 구조 */}
          <div className="weekly-details-grid">
              
              {/* [좌측] 주간 예보 (Weekly Forecast) 영역 */}
              <div className="weekly-forecast-container">
                  <WeeklyForecastList />
              </div>

              {/* [우측] 상세 정보 4가지 및 종합 결과 영역 */}
              <div className="detail-summary-area">
                  
                  {/* 부가 정보 4가지 카드 (UV, 풍속, 미세먼지, 습도) 영역 */}
                  <div className="detail-cards-grid">
                      <DetailCardsGrid />
                  </div>
                  
                  {/* 종합 결과 (야외 활동 최적/무난/비추천) 카드 영역 */}
                  <div className="summary-result-card">
                      <SummaryResultCard />
                  </div>

              </div>

          </div>
          
          {/* 과거 기록 삭제됨 */}

      </div>
      
    </div>
  );
}

export default Dashboard;

