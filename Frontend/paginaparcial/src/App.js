import React from 'react';
import RentMovie from './components/RentMovie';
import Payment from './components/Payment';
import RecentRentals from './components/RecentRentals';

function App() {
    return (
        <div className="App">
            <h1>Rental App</h1>
            <RentMovie />
            <Payment />
            <RecentRentals />
        </div>
    );
}

export default App;
