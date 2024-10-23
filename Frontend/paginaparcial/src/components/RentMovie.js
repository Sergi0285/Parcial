import React, { useState } from 'react';
import { rentMovie } from '../api';

function RentMovie() {
    const [inventoryId, setInventoryId] = useState('');
    const [customerId, setCustomerId] = useState('');
    const [staffId, setStaffId] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await rentMovie({ inventory_id: inventoryId, customer_id: customerId, staff_id: staffId });
            alert('Renta creada exitosamente! ID: ' + response.data.rental_id);
        } catch (error) {
            alert('Error al crear la renta: ' + error.response.data.error);
        }
    };

    return (
        <div>
            <h2>Rentar Película</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="Inventory ID" value={inventoryId} onChange={(e) => setInventoryId(e.target.value)} />
                <input type="text" placeholder="Customer ID" value={customerId} onChange={(e) => setCustomerId(e.target.value)} />
                <input type="text" placeholder="Staff ID" value={staffId} onChange={(e) => setStaffId(e.target.value)} />
                <button type="submit">Rentar</button>
            </form>
        </div>
    );
}

export default RentMovie;
