// src/components/DetailCard.tsx

import React from 'react';
import UVSunIcon from '../assets/UVSunIcon';
import WindIcon from '../assets/WindIcon';
import DustIcon from '../assets/DustIcon';
import HumidityIcon from '../assets/HumidityIcon';

interface DetailMetricData {
    title: string;
    value: string;
    status: string;
    low_high_label: string;
    detail_status: string;
}

interface DetailCardProps {
    dataA: DetailMetricData;
    dataB: DetailMetricData;
}

const getIconComponent = (title: string): React.FC<any> => {
    // ... (기존 스위치 문: 풍속->WindIcon, 자외선->UVSunIcon 등)
    switch (title) {
        case '풍속': return WindIcon;
        case '미세먼지': return DustIcon;
        case '습도': return HumidityIcon;
        case '자외선 지수': return UVSunIcon;
        default: return WindIcon;
    }
};

const DetailCard: React.FC<DetailCardProps> = ({ dataA, dataB }) => {
    if (!dataA || !dataB) return <div>Loading...</div>;
    
    const IconAComponent = getIconComponent(dataA.title);
    const IconBComponent = getIconComponent(dataB.title);

    return (
        <div className="detail-card-container">
            {/* Left Section (dataA) */}
            <div className="detail-item-group left-section">
                 <div className="card-header-group">
                    <IconAComponent size={24} color="#FFF" className="icon-style" /> 
                    <p className="card-title-text">{dataA.title}</p>
                </div>
                <p className="card-value-display">{dataA.value}</p>
                <p className="card-secondary-status">{dataA.low_high_label}</p>
                <p className="card-detail-status">{dataA.detail_status}</p>
            </div>

            {/* Right Section (dataB) */}
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
};

export default DetailCard;