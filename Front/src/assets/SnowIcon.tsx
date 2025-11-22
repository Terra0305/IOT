// src/assets/SnowIcon.tsx

import * as React from "react";

// Props 타입 정의: SVG 기본 속성 + size(선택적)
interface IconProps extends React.SVGProps<SVGSVGElement> {
    size?: number;
}

const SnowIcon = (props: IconProps) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    // size가 있으면 그 값을 쓰고, 없으면 기본값 41
    width={props.size || 41}
    height={props.size ? (props.size / 41) * 49 : 49} 
    viewBox="0 0 41 49"
    fill="none"
    {...props}
  >
    {/* 구름 모양 */}
    <path
      d={`M20.5 0C8.24863 6.15646 0 17.6479 0 30.818C0 31.2888 0.00748127 31.7564 0.029927 32.2207C1.03248 54.5931 39.9675 54.5931 40.9701 32.2207C40.9925 31.7564 41 31.2888 41 30.818C41.0037 17.6479 32.7514 6.15646 20.5 0Z`}
      fill="#A9A9A9" 
    />
    
    {/* 눈송이 3개 */}
    <circle cx="12" cy="40" r="1.5" fill="#FFF" stroke="#000" strokeWidth="0.354"/> 
    <circle cx="20" cy="43" r="2.5" fill="#FFF" stroke="#000" strokeWidth="0.354"/> 
    <circle cx="32" cy="40" r="2" fill="#FFF" stroke="#000" strokeWidth="0.354"/>  
  </svg>
);

export default SnowIcon;