import * as React from "react";

const RainIcon = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    // width와 height를 동적으로 조정하여 비율 유지
    width={props.size || 41}
    height={props.size ? (props.size / 41) * 49 : 49} 
    viewBox="0 0 41 49"
    fill="none"
    {...props}
  >
    {/* 구름 모양 Path (Cloudy 아이콘과 동일한 마스터 컴포넌트) */}
    <path
      d={`M20.5 0C8.24863 6.15646 0 17.6479 0 30.818C0 31.2888 0.00748127 31.7564 0.029927 32.2207C1.03248 54.5931 39.9675 54.5931 40.9701 32.2207C40.9925 31.7564 41 31.2888 41 30.818C41.0037 17.6479 32.7514 6.15646 20.5 0Z`}
      fill={props.color || "white"}
    />
    
    {/* 빗방울 (크기 다르게 3개) */}
    <circle cx="12" cy="40" r="1.5" fill={props.color || "white"} /> {/* Small */}
    <circle cx="20" cy="43" r="2.5" fill={props.color || "white"} /> {/* Large */}
    <circle cx="32" cy="40" r="2" fill={props.color || "white"} />  {/* Medium */}
  </svg>
);

export default RainIcon;