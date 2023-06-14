import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Create a root element for rendering the React app
const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

// Render the app inside a React.StrictMode component
root.render(
  // StrictMode enables additional React checks and warnings for potential issues
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
