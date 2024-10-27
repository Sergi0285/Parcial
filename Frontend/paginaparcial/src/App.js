import React from 'react';
import RecentRentals from './components/RecentRentals';
import Datos from './components/Datos';

function App() {
    return (
        <div className="App">
            <h1>Rental App</h1>
            <Datos />
            <RecentRentals />
        </div>
    );
}

export default App;
