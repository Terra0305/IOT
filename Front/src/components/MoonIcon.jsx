// src/components/icons/MoonIcon.jsx

import * as React from "react";

const MoonIcon = (props) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    width={props.width || 247} 
    height={props.height || 238} 
    viewBox="0 0 247 238" 
    fill="none"
    // Figma의 그림자 효과를 CSS로 전달합니다.
    className={props.className} 
    {...props} 
  >
    {/* 단순한 흰색 원형 달 SVG 경로 (편의상 단순 원으로 대체) */}
    <circle cx="123.5" cy="119" r="119" fill="#FFF" />

    {/* SVG에 직접 그림자 적용 (CSS에서도 가능하지만, SVG 자체에 적용된 경우) */}
    {/* fill 속성 외에 filter: drop-shadow를 CSS에 추가해야 합니다. */}
  </svg>
);

export default MoonIcon;