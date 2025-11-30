import { useState } from 'react';
import Dashboard from './pages/Dashboard.tsx';
import './App.css';
import './styles/variables.css';

const getThemeClass = (isDay: boolean) => {
  return isDay ? 'theme-day-clear' : 'theme-dark';
};

function App() {
  const [isDayTime] = useState<boolean>(true);
  const themeClass = getThemeClass(isDayTime);

  return (
    <div className={`app-container ${themeClass} min-h-screen`}>
      <Dashboard />
    </div>
  );
}

export default App;
