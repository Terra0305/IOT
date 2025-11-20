// src/components/icons/SunIcon.jsx

import * as React from "react";

const SunIcon = (props) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    width={props.width || 128} // 기본값 128
    height={props.height || 120} // 기본값 120
    viewBox="0 0 128 120" 
    fill="none" 
    {...props} // 부모로부터 받은 className 등의 prop 전달
  >
    <path 
      d="M128 60C128 93.1371 99.3462 120 64 120C28.6538 120 0 93.1371 0 60C0 26.8629 28.6538 0 64 0C99.3462 0 128 26.8629 128 60Z" 
      fill="url(#paint0_radial_1_17)" 
      fillOpacity="0.8" 
    />
    <defs>
      <radialGradient 
        id="paint0_radial_1_17" 
        cx={0} cy={0} r={1} 
        gradientUnits="userSpaceOnUse" 
        transform="translate(64 60) rotate(90) scale(83.5135 89.0811)"
      >
        <stop stopColor="#FFD88B" />
        <stop offset={1} stopColor="#FFA900" />
      </radialGradient>
    </defs>
  </svg>
);

export default SunIcon;