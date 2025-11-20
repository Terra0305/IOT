// src/components/SummaryResultCard.jsx

import React from 'react';

// 예시를 위한 더미 데이터 (실제 앱에서는 Props로 받아야 합니다)
const DUMMY_WEATHER_DATA = {
    sky_value: '맑음', // 맑음, 구름 많음, 흐림
    pty_value: '없음', // 비, 눈, 없음 등
    dust_level: '좋음', // 좋음, 보통, 나쁨, 매우 나쁨
    wind_speed: 1.5, // 풍속 (m/s)
};

// --- 1. 무작위 추천 목록 선택 함수 ---

/**
 * 배열에서 지정된 개수만큼 무작위 요소를 선택합니다.
 * @param {Array} arr - 전체 추천 리스트
 * @param {number} count - 선택할 개수 (여기서는 3개)
 * @returns {Array} - 무작위로 선택된 리스트 (새로고침 시마다 변경)
 */
function getRandomRecommendations(arr, count) {
    if (arr.length <= count) return arr; // 리스트가 충분하지 않으면 전체 반환

    // 배열을 무작위로 섞은 후, 앞에서 count 개만 잘라냅니다.
    const shuffled = [...arr].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
}


// --- 2. 날씨 상태별 콘텐츠 맵 (전체 목록 정의) ---
const ACTIVITY_MAP = {
    // 1. 야외 활동 최적 (Good)
    good: {
        emoji: "😎", 
        headline: "야외 활동 최적",
        advice: "미세먼지 좋음, 낮은 풍속으로 공기가 상쾌한 날이에요.",
        recommendation: "테라스 무드를 완성해 줄 추천 음악 🎵", 
        // [수정됨] fullList에 전체 추천 목록을 넣습니다.
        fullList: [
            "Maroon 5 - Sunday Morning", 
            "Lauv - I Like Me Better", 
            "Jeremy Zucker - comethru",
            "why don't we - What Am I",
            "Ceraadi - That's What She'd Say",
            "Hugo Helmig - Champagne Problems",
            "근처 공원에서 피크닉 즐기기", // 활동 추가
            "가벼운 조깅이나 산책 추천" // 활동 추가
        ]
    },

    // 2. 실내 쾌적 지수 최상 (Neutral / 무난) - 작업/운동 추천
    neutral: {
        emoji: "🏠",
        headline: "오늘은 실내 쾌적 지수 최상",
        advice: "바람이 선선하고 습도가 안정적입니다. 창가에 앉아 밀린 일에 집중해 보세요.",
        recommendation: "집중력을 높이는 작업/공부 플레이리스트 🎧",
        // [수정됨] fullList에 전체 추천 목록을 넣습니다.
        fullList: [
            "Lofi Hip Hop - Beats to Relax", 
            "Focus Music - Alpha Waves", 
            "Classical Study Mix",
            "Jazz & Bossa Nova for Focus",
            "재택 근무 환경 정리하기", // 활동 추가
            "밀린 서류 작업 끝내기", 
            "취미 코딩 프로젝트 시작하기",
            "가벼운 홈 트레이닝 추천" // 활동 추가
        ]
    },

    // 3. 실내 활동 권장 (Bad / 안 좋을 때) - 영화, 휴식 추천
    bad: {
        emoji: "☔",
        headline: "실내 활동 권장",
        advice: "비가 오거나 미세먼지가 심해요. 안전을 위해 따뜻한 집에서 휴식이 필요합니다.",
        recommendation: "이런 날 즐기기 좋은 영화/휴식 추천 🍿",
        // [수정됨] fullList에 전체 추천 목록을 넣습니다.
        fullList: [
            "어바웃 타임 (About Time)", // 힐링 코미디
            "인셉션 (Inception)",        // 몰입도 높은 스릴러
            "그랜드 부다페스트 호텔", // 클래식/감성 영화
            "기생충 (Parasite)", // 명작 추천
            "해리 포터 전 시리즈 정주행",
            "따뜻한 코코아 마시기", 
            "퍼즐 맞추기",
            "클래식 소설 다시 읽기" 
        ]
    }
};

/**
 * 날씨 데이터를 분석하여 종합 상태 (good, neutral, bad)를 결정합니다.
 * @param {object} data - API에서 받은 현재 날씨 데이터
 * @returns {object} - 현재 상태에 맞는 ACTIVITY_MAP의 콘텐츠 (무작위 목록 포함)
 */
function getSummaryContent(data) {
    const { pty_value, dust_level, sky_value, wind_speed } = data;
    
    // --- 1. 상태 키 결정 로직 ---
    let statusKey = 'neutral';
    
    // 최악 상태 (Bad) 판정: 비, 눈, 나쁨/매우 나쁨 미세먼지
    if (pty_value !== '없음' || dust_level === '매우 나쁨' || dust_level === '나쁨') {
        statusKey = 'bad';
    } 
    // 최적 상태 (Good) 판정: 맑고, 미세먼지 좋음, 바람 잔잔
    else if (sky_value === '맑음' && dust_level === '좋음' && wind_speed < 3.0) {
        statusKey = 'good';
    }
    // 나머지 경우: Neutral (구름 많음, 보통 미세먼지 등)
    else {
        statusKey = 'neutral';
    }
    
    // --- 2. 콘텐츠 및 무작위 목록 선택 ---
    const baseContent = ACTIVITY_MAP[statusKey];

    // **핵심: 전체 목록(fullList)에서 3개를 무작위로 선택합니다.**
    const randomList = getRandomRecommendations(baseContent.fullList, 3);
    
    // baseContent의 나머지 속성과 무작위로 선택된 list를 합쳐 반환합니다.
    return {
        ...baseContent,
        list: randomList, // 기존 fullList 대신 랜덤 목록으로 덮어씁니다.
    };
}


// --- SummaryResultCard 컴포넌트 정의 ---
function SummaryResultCard({ weatherData = DUMMY_WEATHER_DATA }) {
    
    // 새로고침(컴포넌트 렌더링)할 때마다 getSummaryContent가 호출되어 새로운 목록을 반환합니다.
    const content = getSummaryContent(weatherData); 
    
    return (
        <div className="summary-card-container">
            {/* 1. 제목 및 이모지/표정 영역 */}
            <div className="summary-header">
                <span className="status-emoji">{content.emoji}</span>
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

            {/* 4. 추천 리스트 */}
            <ul className="recommendation-list">
                {content.list.map((item, index) => (
                    // index를 key로 사용하는 것은 좋지 않지만, 여기서는 무작위로 목록이 바뀌므로 허용합니다.
                    <li key={item}>{item}</li> 
                ))}
            </ul>
        </div>
    );
}

export default SummaryResultCard;