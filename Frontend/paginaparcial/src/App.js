import React from 'react';
import RecentRentals from './components/RecentRentals';
import Datos from './components/Datos';
import './App.css';  // Importar los estilos

function App() {
    return (
        <div className="App">
            <h1>Rental App</h1>
            <div className="container">
                <Datos />
                <RecentRentals />
            </div>
        </div>
    );
}

export default App;
