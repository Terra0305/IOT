// src/main.tsx (전체 코드 대체)

import React from 'react'; // [핵심 수정]: React를 명시적으로 임포트
import ReactDOM from 'react-dom/client';
import App from './App.tsx'; 
import './index.css';


ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App /> 
  </React.StrictMode>,
);