import React, { useState } from 'react';
import { makePayment } from '../api';

function Payment() {
    const [rentalId, setRentalId] = useState('');
    const [customerId, setCustomerId] = useState('');
    const [staffId, setStaffId] = useState('');
    const [amount, setAmount] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await makePayment({ rental_id: rentalId, customer_id: customerId, staff_id: staffId, amount });
            alert('Pago registrado exitosamente! ID: ' + response.data.payment_id);
        } catch (error) {
            alert('Error al registrar el pago: ' + error.response.data.error);
        }
    };

    return (
        <div>
            <h2>Registrar Pago</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="Rental ID" value={rentalId} onChange={(e) => setRentalId(e.target.value)} />
                <input type="text" placeholder="Customer ID" value={customerId} onChange={(e) => setCustomerId(e.target.value)} />
                <input type="text" placeholder="Staff ID" value={staffId} onChange={(e) => setStaffId(e.target.value)} />
                <input type="text" placeholder="Amount" value={amount} onChange={(e) => setAmount(e.target.value)} />
                <button type="submit">Registrar Pago</button>
            </form>
        </div>
    );
}

export default Payment;
