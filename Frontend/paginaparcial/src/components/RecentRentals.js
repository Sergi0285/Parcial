import React, { useEffect, useState } from 'react';
import { getRecentRentals } from '../api';

function RecentRentals() {
    const [rentals, setRentals] = useState([]);

    useEffect(() => {
        fetchRecentRentals();
    }, []);

    const fetchRecentRentals = async () => {
        try {
            const response = await getRecentRentals();
            setRentals(response);
        } catch (error) {
            alert('Error al obtener las rentas: ' + error.message);
        }
    };

    return (
        <div>
            <h2>Últimas 20 Películas Rentadas</h2>
            <ul>
                {rentals.map((rental) => (
                    <li key={rental.rental_id}>
                        Rental ID: {rental.rental_id}, Customer ID: {rental.customer_id}, Amount: ${rental.amount}, Payment Date: {rental.payment_date}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default RecentRentals;
