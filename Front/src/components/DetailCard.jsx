// src/components/DetailCard.jsx (수정)

import React from 'react';
import UVSunIcon from '../assets/UVSunIcon';
import UVSunIcon from '../assets/WindIcon';
import UVSunIcon from '../assets/DustIcon';
import UVSunIcon from '../assets/HumidityIcon';


// 2. 제목에 따라 아이콘 컴포넌트를 반환하는 함수
const getIconComponent = (title) => {
    switch (title) {
        case '풍속':
            return WindIcon;
        case '미세먼지':
            return DustIcon;
        case '습도':
            return HumidityIcon;
        case '자외선 지수':
            return UVSunIcon;
        default:
            return WindIcon; 
    }
};

// Props로 dataA (UV)와 dataB (Wind) 두 세트의 정보를 받습니다.
function DetailCard({ dataA, dataB }) {
  
  // 만약 데이터가 하나만 있다면 오류 방지
  if (!dataA || !dataB) return <div className="detail-card-container">Loading...</div>;

  return (
    // 최상위 컨테이너: 가로 분할을 위한 Flexbox (CSS: .detail-card-container)
    <div className="detail-card-container"> 
      
      {/* 1. [좌측] 첫 번째 정보 섹션 (dataA: UV) */}
      <div className="detail-item-group left-section"> 
        
        {/* 헤더 그룹: 아이콘 + 제목 */}
        <div className="card-header-group">
            <IconA size={24} color="#FFF" className="icon-style" />
            <p className="card-title-text">{dataA.title}</p>
        </div>
        
        <p className="card-value-display">{dataA.value}</p>
        <p className="card-status-text">{dataA.status}</p>

      </div> 
      
  {/* 2. [우측] 두 번째 정보 섹션 (dataB: 습도) */}
      <div className="detail-item-group right-section"> 
        
        {/* 헤더 그룹 */}
        <div className="card-header-group">
            {/* 아이콘 컴포넌트 렌더링 */}
            <HumidityIcon size={24} color="#FFF" className="icon-style" /> 
            <p className="card-title-text">{dataB.title}</p>
        </div>
        
        {/* 수치 */}
        <p className="card-value-display">{dataB.value}</p>
        
        {/* 상세 설명 */}
        <p className="card-detail-status">{dataB.status}</p>

      </div>
    </div>
  );
}

export default DetailCard;