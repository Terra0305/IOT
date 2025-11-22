import { useState, useEffect } from 'react'; // Hooks 임포트
import Dashboard from './pages/Dashboard.tsx'; // [중요] Dashboard 페이지 임포트
import './App.css'; 
import './styles/variables.css';

const getThemeClass = (isDay: boolean) => {
  // isDay가 true면 Light Mode, false면 Dark Mode (theme-dark)
  return isDay ? 'theme-day-clear' : 'theme-dark'; 
};

function App() {
  const [isDayTime, setIsDayTime] = useState<boolean>(true); 
  const themeClass = getThemeClass(isDayTime);

  useEffect(() => {
    // WeatherCurrent에서 이미 body.className을 설정하고 있지만, 
    // 여기서는 초기 상태를 설정합니다.
    document.body.className = themeClass;

    return () => {
      document.body.className = '';
    };
  }, [themeClass]);

  return (
    // app-container는 전체 화면 레이아웃을 위한 Wrapper
    <div className="app-container">
      <Dashboard />
    </div>
  );
}

export default App
