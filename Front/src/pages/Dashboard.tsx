import SummaryResultCard from '../components/SummaryResultCard';
import DetailCardsGrid from '../components/DetailCardsGrid';
import WeeklyForecastList from '../components/WeeklyForecastList';
import HourlyForecastList from '../components/HourlyForecastList';
import WeatherCurrent from '../components/WeatherCurrent';
import '../styles/dashboard.css';

export default function Dashboard() {
  const cardStyle = "bg-white/10 backdrop-blur-md rounded-[25px] border border-white/20 p-7 shadow-lg";

  return (
    <div className="w-full max-w-[3600px] mx-auto text-left p-20 flex flex-col gap-15 text-white">
      
      {/* 상단 헤더 영역 (Current Weather) */}
      <div className="w-full flex justify-center mb-[200px]">
         <WeatherCurrent />
      </div>
        

      {/* === [전체 레이아웃: 12칸 그리드] === */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-[65px] items-stretch">
        
        {/* [A. 왼쪽 큰 그룹 (8칸 차지)] */}
        <div className="md:col-span-8 flex flex-col gap-20">
            
            {/* 1. 시간별 예보 (지붕 역할 - 맨 위에 위치) */}
           <div className={`w-full overflow-x-auto overflow-y-hidden min-h-[350px] flex items-center ${cardStyle} px-6`}>
                <HourlyForecastList />
            </div>

            {/* 2. 아래쪽 분할 영역 (주간 vs 상세) */}
            {/* 여기서 주간예보와 상세카드가 4:4 비율로 나뉩니다 (원하시면 3:5, 5:3 등 조절 가능) */}
            <div className="grid grid-cols-1 md:grid-cols-8 gap-[60px] h-full">
                
                {/* 2-1. 주간 예보 (4칸) */}
                <div className={`md:col-span-4 ${cardStyle} h-full`}>
                    <WeeklyForecastList />
                </div>

                {/* 2-2. 상세 카드들 (4칸) - 중앙 정렬 */}
                <div className="md:col-span-4 flex flex-col gap-12 h-full justify-center">
                    <DetailCardsGrid type="UV_WIND" />
                    <DetailCardsGrid type="DUST_HUMIDITY" />
                </div>
            </div>

        </div>

        {/* [B. 오른쪽 활동 추천 (4칸 차지)] */}
        <div className="md:col-span-4 h-full">
             <SummaryResultCard />
        </div>

      </div>

    </div>
  );
}