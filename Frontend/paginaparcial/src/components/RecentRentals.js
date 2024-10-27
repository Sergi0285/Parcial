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
            {rentals.length === 0 ? (
                <p>No hay rentas recientes disponibles.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Rental ID</th>
                            <th>Nombre del Cliente</th>
                            <th>Título de la Película</th>
                            <th>Monto</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rentals.map((rental) => (
                            <tr key={rental.rental_id}>
                                <td>{rental.rental_id}</td>
                                <td>{rental.customer_full_name}</td>
                                <td>{rental.film_title}</td>
                                <td>${rental.amount}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default RecentRentals;
