// src/components/icons/PartlyCloudyIcon.jsx (최종 통합 구조)

import React from 'react';
import SunIcon from './SunIcon';
import CloudIconLarge from './CloudIconLarge'; // (가정: 큰 구름 파일)
import CloudIconSmall from './CloudIconSmall'; // (가정: 작은 구름 파일)


function PartlyCloudyIcon(props) {
  return (
    // position: relative를 사용하여 내부 요소의 절대 위치 기준점을 잡습니다.
    <div className="partly-cloudy-icon-wrapper">
        
        {/* 1. 해 아이콘 (배경에 깔림) - z-index: 1 */}
        <SunIcon className="partly-sun-base" {...props} /> 
        
        {/* 2. 큰 구름 (해를 가림) - z-index: 5 */}
        <CloudIconLarge className="cloud-layer-1" {...props} /> 
        
        {/* 3. 작은 구름 (가장 위에 겹쳐져 깊이감을 더함) - z-index: 10 */}
        <CloudIconSmall className="cloud-layer-2" {...props} />
        
    </div>
  );
}

export default PartlyCloudyIcon;