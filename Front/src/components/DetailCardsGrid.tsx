import React from 'react';

interface DetailCardsGridProps {
  type?: 'UV_WIND' | 'DUST_HUMIDITY';
}

export default function DetailCardsGrid({ type }: DetailCardsGridProps) {

  // 1. 자외선 & 풍속 카드
  if (type === 'UV_WIND') {
    return (
      <div className="detail-card-container">
        
        {/* [왼쪽] 자외선 */}
        {/* !justify-center: 내용을 중앙에 모음 */}
        <div className="detail-item-group left-section !justify-center flex flex-col">
            
            {/* 1. 제목 */}
            {/* [간격] 제목과 숫자 사이: mb-4 (16px) */}
            <div className="card-header-group mb-4">
                <span className="text-[40px] font-bold text-white/90">
                    자외선 지수
                </span>
            </div>

            {/* 2. 숫자 값 */}
            {/* [간격] 숫자와 상태(LOW) 사이: mb-6 (넓게 24px) */}
            <div className="card-value-display mb-6">
                1
            </div>

            {/* 3. 상태 (LOW) */}
            {/* [간격] 상태와 설명 사이: mb-1 (딱 붙임) */}
            <p className="card-detail-status mb-1">
                LOW
            </p>

            {/* 4. 설명 */}
            <p className="card-secondary-status">
                자외선 지수가 낮음
            </p>
        </div>

        {/* [오른쪽] 풍속 */}
        <div className="detail-item-group right-section !justify-center flex flex-col">
            
            {/* 1. 제목 */}
            <div className="card-header-group mb-5">
                <span className="text-[40px] font-bold text-white/90">
                    풍속
                </span>
            </div>

            {/* 2. 숫자 값 */}
            <div className="card-value-display mb-6">
                5 km/h
            </div>

            {/* 3. 상태 */}
            <p className="card-detail-status mb-1">
                LOW
            </p>

            {/* 4. 설명 */}
            <p className="card-secondary-status">
                바람이 잔잔합니다
            </p>
        </div>
      </div>
    );
  }

  // 2. 미세먼지 & 습도 카드
  if (type === 'DUST_HUMIDITY') {
    return (
      <div className="detail-card-container">
        
        {/* [왼쪽] 미세먼지 */}
        <div className="detail-item-group left-section !justify-center flex flex-col">
            
            {/* 1. 제목 */}
            <div className="card-header-group mb-7">
                <span className="text-[40px] font-bold text-white/90">
                    미세먼지
                </span>
            </div>

            {/* 2. 숫자 값 */}
            <div className="card-value-display mb-10">
                12 µg/m³
            </div>

            {/* 3. 상태 */}
            <p className="card-detail-status mb-3">
                GOOD
            </p>

            {/* 4. 설명 */}
            <p className="card-secondary-status">
                공기질이 깨끗합니다
            </p>
        </div>

        {/* [오른쪽] 습도 */}
        <div className="detail-item-group right-section !justify-center flex flex-col">
            
            {/* 1. 제목 */}
            <div className="card-header-group mb-7">
                <span className="text-[40px] font-bold text-white/90">
                    습도
                </span>
            </div>

            {/* 2. 숫자 값 */}
            <div className="card-value-display mb-11">
                61%
            </div>

            {/* 3. 상태 */}
            <p className="card-detail-status mb-2">
                NORMAL
            </p>

            {/* 4. 설명 */}
            <p className="card-secondary-status">
                습도가 적당합니다
            </p>
        </div>
      </div>
    );
  }

  return null;
}