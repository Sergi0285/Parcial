import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Usa createRoot en lugar de ReactDOM.render
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
