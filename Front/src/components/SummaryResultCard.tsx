// src/components/SummaryResultCard.tsx (전체 코드)

import React from 'react';
import SummaryStatusIcon from './SummaryStatusIcon'; // 아이콘 컴포넌트 임포트 (경로 확인)

// --- [Type Definition] 데이터 타입 정의 ---

// 1. 날씨 데이터 타입
interface WeatherData {
    sky_value: string;
    pty_value: string;
    dust_level: string;
    wind_speed: number;
}

// 2. 활동 추천 콘텐츠 타입
interface ActivityContent {
    emoji: string;
    headline: string;
    advice: string;
    recommendation: string;
    fullList: string[];
    list?: string[]; // 랜덤 선택 후 추가될 필드 (선택적)
}

// 3. 상태 키 타입 ('good' | 'neutral' | 'bad' 만 허용)
type StatusKey = 'good' | 'neutral' | 'bad';


// --- 예시 더미 데이터 ---
const DUMMY_WEATHER_DATA: WeatherData = {
    sky_value: '맑음',
    pty_value: '없음',
    dust_level: '좋음',
    wind_speed: 1.5,
};

// --- 1. 무작위 추천 목록 선택 함수 ---
// [Error 7006 해결]: 매개변수 arr와 count에 타입 명시
function getRandomRecommendations(arr: string[], count: number): string[] {
    if (arr.length <= count) return arr; 
    const shuffled = [...arr].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
}


// --- 2. 날씨 상태별 콘텐츠 맵 ---
// [Error 7053 해결]: Record<StatusKey, ActivityContent> 타입 명시
const ACTIVITY_MAP: Record<StatusKey, ActivityContent> = {
    good: {
        emoji: "good", // SVG 아이콘 status 키
        headline: "야외 활동 최적",
        advice: "미세먼지 좋음, 낮은 풍속으로 공기가 상쾌한 날이에요.",
        recommendation: "테라스 무드를 완성해 줄 추천 음악 🎵", 
        fullList: [
            "Maroon 5 - Sunday Morning", 
            "Lauv - I Like Me Better", 
            "Jeremy Zucker - comethru",
            "Ed Sheeran - Perfect",
            "Bruno Mars - Just the Way You Are",
            "The Chainsmokers - Closer",
            "근처 공원에서 피크닉 즐기기", 
            "가벼운 조깅이나 산책 추천"
        ]
    },
    neutral: {
        emoji: "neutral", // SVG 아이콘 status 키
        headline: "오늘은 실내 쾌적 지수 최상",
        advice: "바람이 선선하고 습도가 안정적입니다. 창가에 앉아 밀린 일에 집중해 보세요.",
        recommendation: "집중력을 높이는 작업/공부 플레이리스트 🎧",
        fullList: [
            "Lofi Hip Hop - Beats to Relax", 
            "Focus Music - Alpha Waves", 
            "Classical Study Mix",
            "Jazz & Bossa Nova for Focus",
            "재택 근무 환경 정리하기", 
            "밀린 서류 작업 끝내기", 
            "취미 코딩 프로젝트 시작하기",
            "가벼운 홈 트레이닝 추천"
        ]
    },
    bad: {
        emoji: "bad", // SVG 아이콘 status 키
        headline: "실내 활동 권장",
        advice: "비가 오거나 미세먼지가 심해요. 안전을 위해 따뜻한 집에서 휴식이 필요합니다.",
        recommendation: "이런 날 즐기기 좋은 영화/휴식 추천 🍿",
        fullList: [
            "어바웃 타임 (About Time)", 
            "인셉션 (Inception)",        
            "그랜드 부다페스트 호텔", 
            "기생충 (Parasite)", 
            "해리 포터 전 시리즈 정주행",
            "따뜻한 코코아 레시피 만들기", 
            "퍼즐 맞추기 챌린지 시작",
            "클래식 소설 다시 읽기" 
        ]
    }
};

// [Error 7006 해결]: data 매개변수 타입 명시
function getSummaryContent(data: WeatherData): ActivityContent {
    const { pty_value, dust_level, sky_value, wind_speed } = data;
    
    // --- 1. 상태 키 결정 로직 ---
    let statusKey: StatusKey = 'neutral'; // 초기값 타입 명시
    
    if (pty_value !== '없음' || dust_level === '매우 나쁨' || dust_level === '나쁨') {
        statusKey = 'bad';
    } 
    else if (sky_value === '맑음' && dust_level === '좋음' && wind_speed < 3.0) {
        statusKey = 'good';
    }
    else {
        statusKey = 'neutral';
    }
    
    // --- 2. 콘텐츠 및 무작위 목록 선택 ---
    // [Error 7053 해결]: statusKey가 StatusKey 타입이므로 안전하게 접근 가능
    const baseContent = ACTIVITY_MAP[statusKey];

    const randomList = getRandomRecommendations(baseContent.fullList, 3);
    
    return {
        ...baseContent,
        list: randomList, 
    };
}

// --- Component Props Type ---
interface SummaryResultCardProps {
    weatherData?: WeatherData;
}

// --- SummaryResultCard 컴포넌트 정의 ---
const SummaryResultCard: React.FC<SummaryResultCardProps> = ({ weatherData = DUMMY_WEATHER_DATA }) => {
    
    const content = getSummaryContent(weatherData); 
    
    return (
        <div className="summary-card-container">
            {/* 1. 제목 및 이모지/표정 영역 */}
            <div className="summary-header">
                {/* SummaryStatusIcon 컴포넌트 사용 (emoji 키 전달) */}
                <SummaryStatusIcon status={content.emoji} size={70} />
                <h3 className="status-headline">{content.headline}</h3>
            </div>
            
            {/* 2. 상세 근거 */}
            <p className="summary-advice-text">
                {content.advice}
            </p>
            
            {/* 3. 추천 목록 제목 */}
            <p className="summary-recommend-title">
                {content.recommendation}
            </p>

            {/* 4. 추천 리스트 (content.list가 존재할 때만 렌더링) */}
            <ul className="recommendation-list">
                {content.list && content.list.map((item, index) => (
                    <li key={index}>{item}</li> 
                ))}
            </ul>
        </div>
    );
}

export default SummaryResultCard;