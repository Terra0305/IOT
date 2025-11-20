// src/assets/icons/MoonCloudyIcon.jsx (밤 흐림 아이콘 - 달 구름)

import * as React from "react";
// 구름 아이콘은 기존에 정의된 것을 사용한다고 가정합니다.
import CloudIcon from './CloudIcon'; // CloudIcon을 임포트 (아직 생성 전이라면 가상으로 추가)

const MoonCloudyIcon = (props) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    width={props.width || 196} 
    height={props.height || 167} 
    viewBox="0 0 196 167" 
    fill="none"
    {...props} 
  >
    {/* 달 모양 Path */}
    <path 
      fillRule="evenodd" 
      clipRule="evenodd" 
      d="M195.86 124.117C183.753 128.096 170.535 130.286 156.692 130.286C98.5492 130.286 51.4148 91.6538 51.4148 43.9985C51.4148 27.9277 56.7752 12.883 66.1104 0C27.3633 12.7366 0 43.8083 0 80.1183C0 127.773 47.1344 166.406 105.278 166.406C143.813 166.406 177.513 149.436 195.86 124.117Z" 
      fill="#BAC7CB" // Figma의 단일 fill 색상 적용
    />
    
    {/* 구름은 별도의 CloudIcon 컴포넌트를 사용하여 달 위에 겹쳐서 표시합니다. */}
    {/* 위치와 크기는 CSS 또는 직접 조정이 필요합니다. */}
    {/* 예: <CloudIcon style={{ position: 'absolute', top: '20px', left: '80px', zIndex: 1 }} size={100} color="white" /> */}
    {/* 여기서는 MoonCloudyIcon 자체에 구름 SVG를 포함시키거나,
       WeatherCurrent에서 두 아이콘을 겹쳐 그리는 방식 중 하나를 선택해야 합니다.
       일단 MoonCloudyIcon은 달만 포함하고, WeatherCurrent에서 구름을 추가하겠습니다.
    */}
  </svg>
);

export default MoonCloudyIcon;