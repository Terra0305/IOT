import { useEffect, useState } from 'react';
import axios from 'axios';

// --- [Type Definition] 데이터 타입 정의 ---
interface WeatherData {
    sky_value: string;
    pty_value: string;
    dust_level: string;
    wind_speed: number;
}

interface ActivityContent {
    emoji: string;
    headline: string;
    advice: string;
    suggestion?: string;
    recommendation: string;
    recommendationSub?: string;
    fullList: string[];
    list?: string[];
}
type StatusKey = 'good' | 'neutral' | 'bad';

// --- 예시 더미 데이터 ---
const DUMMY_WEATHER_DATA: WeatherData = {
    sky_value: '맑음',
    pty_value: '없음',
    dust_level: '좋음',
    wind_speed: 1.5,
};

// --- 1. 무작위 추천 목록 선택 함수 ---
function getRandomRecommendations(arr: string[], count: number): string[] {
    if (arr.length <= count) return arr;
    const shuffled = [...arr].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, count);
}

// --- 2. 날씨 상태별 콘텐츠 맵 ---
const ACTIVITY_MAP: Record<StatusKey, ActivityContent> = {
    good: {
        emoji: "😊",
        headline: "야외 활동 최적",
        advice: "미세먼지 좋음, 낮은 풍속으로 공기가 상쾌한 날이에요. ☀️",
        suggestion: "좋은 날씨에 야외 활동이나 테라스에서 커피 한 잔 어떠세요?",
        recommendation: "테라스 무드를 완성해 줄 추천 음악 🎵",
        recommendationSub: "또는 야외 활동 🛼",
        fullList: [
            "Maroon 5 - Sunday Morning",
            "Lauv - I Like Me Better",
            "Jeremy Zucker - comethru",
            "Ed Sheeran - Perfect",
            "Bruno Mars - Just the Way You Are",
            "근처 공원에서 피크닉 즐기기",
            "가벼운 조깅이나 산책 추천"
        ]
    },
    neutral: {
        emoji: "😐",
        headline: "실내 쾌적 지수 최상",
        advice: "바람이 선선하고 습도가 안정적입니다.",
        suggestion: "창가에 앉아 밀린 일에 집중해 보는 건 어떨까요?",
        recommendation: "집중력을 높이는 플레이리스트 🎧",
        fullList: [
            "Lofi Hip Hop - Beats to Relax",
            "Focus Music - Alpha Waves",
            "Classical Study Mix",
            "재택 근무 환경 정리하기",
            "밀린 서류 작업 끝내기"
        ]
    },
    bad: {
        emoji: "☔",
        headline: "실내 활동 권장",
        advice: "비가 오거나 날씨가 궂어요.",
        suggestion: "안전을 위해 따뜻한 집에서 휴식이 필요합니다.",
        recommendation: "집콕하며 즐기기 좋은 영화/휴식 🍿",
        fullList: [
            "어바웃 타임 (About Time)",
            "인셉션 (Inception)",
            "기생충 (Parasite)",
            "따뜻한 코코아 마시기"
        ]
    }
};

// --- 3. 로직 함수 ---
function getSummaryContent(data: WeatherData): ActivityContent {
    const { pty_value, dust_level, sky_value, wind_speed } = data;

    let statusKey: StatusKey = 'neutral';

    // 나쁨 조건: 비/눈이 오거나, 미세먼지가 나쁨/매우나쁨
    if (pty_value !== '없음' || dust_level === '매우 나쁨' || dust_level === '나쁨') {
        statusKey = 'bad';
    }
    // 좋음 조건: 맑음 + 미세먼지 좋음/보통 + 바람 약함 (< 5m/s)
    else if (sky_value === '맑음' && (dust_level === '좋음' || dust_level === '보통') && wind_speed < 5.0) {
        statusKey = 'good';
    }

    const baseContent = ACTIVITY_MAP[statusKey];
    const randomList = getRandomRecommendations(baseContent.fullList, 3);

    return {
        ...baseContent,
        list: randomList,
    };
}

// Helper functions for mapping
const getSkyState = (skyCode: string): string => {
    if (skyCode === "1") return "맑음";
    if (skyCode === "3") return "구름많음";
    if (skyCode === "4") return "흐림";
    return "맑음";
};

const getPtyState = (ptyCode: string): string => {
    if (ptyCode === "1") return "비";
    if (ptyCode === "2") return "비/눈";
    if (ptyCode === "3") return "눈";
    if (ptyCode === "4") return "소나기";
    return "없음";
};

const getDustLevel = (grade: string): string => {
    if (grade === "1") return "좋음";
    if (grade === "2") return "보통";
    if (grade === "3") return "나쁨";
    if (grade === "4") return "매우 나쁨";
    return "보통";
};

export default function SummaryResultCard() {
    const [weatherData, setWeatherData] = useState<WeatherData>(DUMMY_WEATHER_DATA);

    useEffect(() => {
        const baseUrl = import.meta.env.VITE_APP_API_URL ?? 'http://localhost:8000';

        const fetchData = async () => {
            try {
                // 1. 날씨 데이터
                const weatherRes = await axios.get(`${baseUrl}/api/weather/current`);
                const weather = weatherRes.data.weather;

                // 2. 미세먼지 데이터
                const dustRes = await axios.get(`${baseUrl}/api/weather/dust`);
                const dust = dustRes.data;

                if (weather && dust) {
                    setWeatherData({
                        sky_value: getSkyState(weather.SKY),
                        pty_value: getPtyState(weather.PTY),
                        dust_level: getDustLevel(dust.pm10Grade),
                        wind_speed: parseFloat(weather.WSD || "0")
                    });
                }
            } catch (error) {
                console.error("Failed to fetch summary data:", error);
            }
        };

        fetchData();
    }, []);

    const content = getSummaryContent(weatherData);

    return (
        <div className="summary-card-container h-full flex flex-col">

            {/* [간격 A] 헤더와 내용 사이 */}
            <div className="flex items-center gap-5 border-b border-white/30 pb-6 mb-[70px]">
                <span className="text-[80px] leading-none">{content.emoji}</span>
                <h2 className="text-[45px] font-bold text-white whitespace-nowrap m-0">
                    {content.headline}
                </h2>
            </div>

            <div className="flex flex-col text-white">

                {/* 1. 날씨 상태 */}
                <p className="text-[39px] leading-relaxed font-medium mb-[150px] opacity-90">
                    {content.advice}
                </p>

                {/* 2. 제안 멘트 */}
                {content.suggestion && (
                    <p className="text-[38px] leading-relaxed font-medium mb-20">
                        {content.suggestion}
                    </p>
                )}

                {/* 3. 추천 제목 1줄 */}
                <p className="text-[37px] font-bold mb-4">
                    {content.recommendation}
                </p>

                {/* 4. 추천 제목 2줄 */}
                {content.recommendationSub && (
                    <p className="text-[37px] font-bold mb-[68px]">
                        {content.recommendationSub}
                    </p>
                )}

                {/* 5. 리스트 */}
                <ul className="list-none p-0 m-0 opacity-90">
                    {content.list?.map((item, index) => (
                        <li key={index} className="text-[38px] mb-7 font-light">
                            {item}
                        </li>
                    ))}
                </ul>
            </div>

        </div>
    );
}