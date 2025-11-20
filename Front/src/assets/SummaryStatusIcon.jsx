// src/components/SummaryStatusIcon.jsx

import * as React from "react";

// 1. 상태별 SVG 경로, 색상, 크기를 분리하여 정의합니다.
//    (주의: Neutral과 Bad의 눈/입 경로 데이터가 필요합니다. 여기서는 외곽원만 사용)
const STATUS_MAP = {
    // 1. GOOD (Green/Smile)
    good: {
        color: "#A6F9C5",
        // 외곽원과 웃는 입/눈의 경로 데이터
        path: "M47.895... [대시보드 외곽 경로] ...M27.9388... [눈과 웃는 입 경로]...",
        size: 77.5
    },
    // 2. NEUTRAL (Dark Gray/Neutral Face)
    neutral: {
        color: "#424866",
        // 외곽원과 무표정한 입/눈의 경로 데이터
        path: "M57.68... [대시보드 외곽 경로] ...M32.6667... [눈과 무표정 입 경로]...",
        size: 94
    },
    // 3. BAD (Dark Gray/Frowning Face)
    bad: {
        color: "#424866",
        // 외곽원과 찡그린 입/눈의 경로 데이터
        path: "M26.4134... [대시보드 외곽 경로] ...M61.9267... [눈과 찡그린 입 경로]...",
        size: 94
    }
};


const SummaryStatusIcon = ({ status, ...props }) => {
    // status prop에 따라 표시할 데이터 선택 (good, bad, neutral)
    const currentStatus = STATUS_MAP[status] || STATUS_MAP.good;

    return (
        <svg 
            xmlns="http://www.w3.org/2000/svg" 
            width={props.size || currentStatus.size} 
            height={props.size || currentStatus.size} 
            viewBox={`0 0 ${currentStatus.size} ${currentStatus.size}`} 
            fill="none"
            {...props} 
        >
            {/* pathData를 사용하여 아이콘 경로를 렌더링 */}
            <path 
                d={currentStatus.path} 
                fill={currentStatus.color} 
            />
        </svg>
    );
};

export default SummaryStatusIcon;