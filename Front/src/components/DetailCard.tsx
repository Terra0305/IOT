// src/components/DetailCard.tsx (전체 내용 대체)

import React from 'react';

// [1. 아이콘 Import] - .jsx 확장자를 그대로 사용하되, TypeScript가 인식하도록 선언 파일을 만들었습니다.
import UVSunIcon from '../assets/UVSunIcon.jsx';
import WindIcon from '../assets/WindIcon.jsx'; 
import DustIcon from '../assets/DustIcon.jsx';
import HumidityIcon from '../assets/HumidityIcon.jsx';

// --- 데이터 타입 Interface 정의 (Error 7031, 7006 해결) ---
interface DetailMetricData {
    title: string;
    value: string;
    status: string;
    low_high_label: string; // LOW / HIGH 레이블
    detail_status: string; // 상세 설명 (예: 바람이 잔잔합니다)
}

interface DetailCardProps {
    dataA: DetailMetricData; // 좌측 항목
    dataB: DetailMetricData; // 우측 항목
}

// --- Icon Component Selector Function ---
// [2. 타입 명시] title은 string임을 명시합니다.
const getIconComponent = (title: string): React.FC<any> => {
    switch (title) {
        case '자외선 지수':
            return UVSunIcon; 
        case '풍속':
            return WindIcon;
        case '미세먼지':
            return DustIcon;
        case '습도':
            return HumidityIcon;
        default:
            return WindIcon; 
    }
};

// --- DetailCard Component Definition (React.FC 적용) ---
// [3. 타입 적용] DetailCard에 Props 타입 적용
const DetailCard: React.FC<DetailCardProps> = ({ dataA, dataB }) => {
    
    // [4. Logic Fix]: 데이터를 받아서 아이콘 컴포넌트를 결정
    const IconAComponent = getIconComponent(dataA.title);
    const IconBComponent = getIconComponent(dataB.title); 

    // 데이터가 없으면 로딩/에러 화면 (JSX)
    if (!dataA || !dataB) return <div className="loading-spinner">Loading...</div>;


    return (
        <div className="detail-card-container"> 
            
            {/* 1. [좌측] 섹션 (dataA) */}
            <div className="detail-item-group left-section"> 
                <div className="card-header-group">
                    <IconAComponent size={24} color="#FFF" className="icon-style" /> 
                    <p className="card-title-text">{dataA.title}</p>
                </div>
                
                {/* 4가지 텍스트 요소 렌더링 */}
                <p className="card-value-display">{dataA.value}</p>
                <p className="card-secondary-status">{dataA.low_high_label}</p>
                <p className="card-detail-status">{dataA.detail_status}</p> 

            </div> 
            
            {/* 2. [우측] 섹션 (dataB) */}
            <div className="detail-item-group right-section"> 
                <div className="card-header-group">
                    <IconBComponent size={24} color="#FFF" className="icon-style" />
                    <p className="card-title-text">{dataB.title}</p>
                </div>
                
                <p className="card-value-display">{dataB.value}</p>
                <p className="card-secondary-status">{dataB.low_high_label}</p>
                <p className="card-detail-status">{dataB.detail_status}</p>

            </div>
        </div>
    );
}

export default DetailCard;