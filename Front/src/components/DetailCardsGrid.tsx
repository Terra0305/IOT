import React from 'react';
import DetailCard from './DetailCard';

// 데이터 타입 정의 (DetailCard의 인터페이스와 일치해야 함)
interface DetailMetricData {
    title: string;
    value: string;
    status: string;
    low_high_label: string;
    detail_status: string;
}

// 더미 데이터 (UV, Wind, Dust, Humidity)
const DUMMY_DETAIL_DATA: DetailMetricData[] = [
    { 
        title: '자외선 지수', 
        value: '1', 
        status: '낮게 유지됩니다', 
        low_high_label: 'LOW', 
        detail_status: '자외선 지수가 낮음' 
    },
    { 
        title: '풍속', 
        value: '5 km/h', 
        status: '바람이 잔잔합니다', 
        low_high_label: 'LOW', 
        detail_status: '바람이 약하게 붑니다' 
    },
    { 
        title: '미세먼지', 
        value: '12 ㎍/㎥', 
        status: '매우 좋음', 
        low_high_label: 'GOOD', 
        detail_status: '공기질이 깨끗합니다' 
    },
    { 
        title: '습도', 
        value: '61%', 
        status: '쾌적한 습도', 
        low_high_label: 'NORMAL', 
        detail_status: '습도가 적당합니다' 
    },
];

// 데이터를 2개씩 묶어서 DetailCard에 전달하기 위한 배열 생성
const DUMMY_DETAIL_DATA_PAIRS = [
    { dataA: DUMMY_DETAIL_DATA[0], dataB: DUMMY_DETAIL_DATA[1] }, // UV + Wind
    { dataA: DUMMY_DETAIL_DATA[2], dataB: DUMMY_DETAIL_DATA[3] }  // Dust + Humidity
];

const DetailCardsGrid: React.FC = () => {
    return (
        <div className="detail-grid-container">
            {DUMMY_DETAIL_DATA_PAIRS.map((pair, index) => (
                <DetailCard
                    key={index}
                    dataA={pair.dataA}
                    dataB={pair.dataB}
                />
            ))}
        </div>
    );
};

export default DetailCardsGrid;