import './App.css'; 
import './styles/themes.css';


import React, { useState, useEffect } from 'react';
import Dashboard from './pages/Dashboard'; 
import './App.css'; 
import './styles/variables.css'; 

// ----------------------------------------------------
// Day/Night 테마 결정 (더미 로직)
// ----------------------------------------------------
const getThemeClass = (isDay) => {
  // isDay가 true면 Light Mode(Day), false면 Dark Mode(Night)
  return isDay ? '' : 'theme-dark'; 
};

function App() {
  // 실제 백엔드 데이터가 들어오면 이 값은 API 응답에 따라 바뀝니다.
  const [isDayTime, setIsDayTime] = useState(true); // 일단 낮(Day)으로 시작
  const themeClass = getThemeClass(isDayTime);

  // 1. 테마 CSS 클래스를 body 태그에 적용하는 로직 (배경색 변경)
  useEffect(() => {
    document.body.className = themeClass;

    // 컴포넌트가 사라질 때 (cleanup) 클래스 제거
    return () => {
      document.body.className = '';
    };
  }, [themeClass]); 

  return (
    <div className="app-container">
      {/* 2. Dashboard 페이지 렌더링 */}
      <Dashboard />
    </div>
  );
}

export default App;