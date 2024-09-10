import React from 'react';
import Usuario from './components/Usuario';
import './App.css'; // Asegúrate de importar el CSS

function App() {
  return (
    <div className="app-container">
      <h1 className="app-title">Aplicación de Usuarios</h1>
      <Usuario />
    </div>
  );
}

export default App;
