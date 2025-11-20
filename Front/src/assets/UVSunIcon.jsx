// src/components/DetailCard.jsx

import React from 'react';
// 1. react-icons에서 태양 아이콘을 임포트합니다.
import { FaSun } from 'react-icons/fa'; 


function DetailCard({ dataA, dataB }) {
  
  // UV 카드 섹션에서 아이콘을 직접 렌더링하는 부분
  const UVIconComponent = dataA.title === '자외선 지수' ? FaSun : <p>🌞</p>; 
  
  return (
    <div className="detail-card-container"> 
      
      {/* 1. [좌측] 첫 번째 정보 섹션 (dataA) */}
      <div className="detail-item-group left-section"> 
        
        <div className="card-header-group">
            {/* 2. UVSunIcon 대신 FaSun 아이콘 사용 */}
            <FaSun size={24} color="#FFF" className="icon-style" /> 
            <p className="card-title-text">{dataA.title}</p>
        </div>
        
        {/* ... (나머지 내용) ... */}
      </div> 
      
      {/* ... (오른쪽 섹션 유지) ... */}
    </div>
  );
}

export default DetailCard;