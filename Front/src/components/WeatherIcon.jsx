import * as React from "react";

// WeatherCondition 타입 정의 (TypeScript 환경을 위한 주석)
// type WeatherCondition = "sun" | "cloud_sun" | "cloud" | "moon" | "sunrise_sunset" | "rain" | "snow";

export const ICON_MAP = {
    // 1. 해 (Sun)
    sun: {
        viewBox: "0 0 100 100",
        paths: [
            // 태양 원형
            { d: "M50 50 A20 20 0 1 0 50 50", fill: "#FFD700" }, 
            // 태양 광선 (수직/수평)
            { d: "M50 10v10 M50 80v10 M10 50h10 M80 50h10", stroke: "#FFD700", strokeWidth: "5", strokeLinecap: "round" },
            // 태양 광선 (대각선)
            { d: "M26.8 26.8l7.07 7.07 M66.13 66.13l7.07 7.07 M26.8 73.2l7.07-7.07 M66.13 33.87l7.07-7.07", stroke: "#FFD700", strokeWidth: "5", strokeLinecap: "round" }
        ]
    },

    // 2. 구름해 (Cloudy Sun)
    cloud_sun: {
        viewBox: "0 0 100 100",
        paths: [
            // 태양 원형 (일부만 보임)
            { d: "M75 30 A18 18 0 1 0 75 30", fill: "#FFD700" }, 
            // 구름
            { d: "M70 65 C70 65 65 45 45 45 C25 45 20 65 20 65 C15 80 30 90 45 90 C60 90 75 80 75 65 Z", fill: "#D3D3D3" }
        ]
    },

    // 3. 구름 (Cloud)
    cloud: {
        viewBox: "0 0 100 100",
        paths: [
            // 구름
            { d: "M70 50 C70 50 65 30 45 30 C25 30 20 50 20 50 C15 65 30 75 45 75 C60 75 75 65 75 50 Z", fill: "#A9A9A9" }
        ]
    },

    // 4. 달 (Moon) - 맑은 밤하늘
    moon: {
        viewBox: "0 0 100 100",
        paths: [
            // 초승달
            { d: "M50 25 A25 25 0 1 0 50 75 A20 20 0 1 1 50 25 Z", fill: "#F0F8FF" }
        ]
    },
    
    // 5. 일출/일몰 (Sunrise/Sunset) - 아이콘 동일
    sunrise_sunset: {
        viewBox: "0 0 100 100",
        paths: [
            // 태양 (수평선 위로 반만)
            { d: "M50 80 A30 30 0 0 0 20 80 H80 A30 30 0 0 0 50 80 Z", fill: "#FF8C00" },
            // 수평선 (Horizon Line)
            { d: "M10 80 H90", stroke: "#8B4513", strokeWidth: "4" }
        ]
    },

    // 6. 비 (Rain)
    rain: {
        viewBox: "0 0 100 100",
        paths: [
            // 구름
            { d: "M70 50 C70 50 65 30 45 30 C25 30 20 50 20 50 C15 65 30 75 45 75 C60 75 75 65 75 50 Z", fill: "#A9A9A9" },
            // 빗방울 (세로선)
            { d: "M35 80v10 M50 85v10 M65 80v10", stroke: "#4169E1", strokeWidth: "4", strokeLinecap: "round" }
        ]
    },

    // 7. 눈 (Snow)
    snow: {
        viewBox: "0 0 100 100",
        paths: [
            // 구름
            { d: "M70 50 C70 50 65 30 45 30 C25 30 20 50 20 50 C15 65 30 75 45 75 C60 75 75 65 75 50 Z", fill: "#A9A9A9" },
            // 눈송이 (별 모양)
            { d: "M35 85 L30 90 L40 90 Z M55 85 L50 90 L60 90 Z M45 80 V90 M40 85 H50 M35 75 L45 85", fill: "#FFFFFF", stroke: "#FFFFFF", strokeWidth: "1" },
            { d: "M35 85 L30 90 L40 90 Z M55 85 L50 90 L60 90 Z M35 75 L45 85", fill: "#FFFFFF", stroke: "#FFFFFF", strokeWidth: "1" },
            { d: "M30 80 H40 M35 75 V85", stroke: "#FFFFFF", strokeWidth: "2", strokeLinecap: "round" },
            { d: "M55 80 H65 M60 75 V85", stroke: "#FFFFFF", strokeWidth: "2", strokeLinecap: "round" }
        ]
    }
};

/**
 * 시간별/주간별 날씨 아이콘을 렌더링하는 컴포넌트
 * @param {object} props
 * @param {WeatherCondition} props.condition - 날씨 상태 ('sun', 'rain', 'snow' 등)
 * @param {number} [props.size] - 아이콘의 크기 (px)
 */
const WeatherIcon = ({ condition, size = 50, ...props }) => {
    // 1. 조건에 맞는 아이콘 데이터 선택 (조건이 없으면 기본 'sun' 사용)
    const iconData = ICON_MAP[condition] || ICON_MAP.sun;

    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width={size}
            height={size}
            viewBox={iconData.viewBox}
            fill="none"
            {...props}
        >
            {/* 2. Paths 배열을 순회하며 모든 경로(도형) 렌더링 */}
            {iconData.paths.map((path, index) => (
                <path
                    key={index}
                    d={path.d}
                    fill={path.fill || "none"}
                    stroke={path.stroke || "none"}
                    strokeWidth={path.strokeWidth || "none"}
                    strokeLinecap={path.strokeLinecap || "none"}
                />
            ))}
        </svg>
    );
};

export default WeatherIcon;