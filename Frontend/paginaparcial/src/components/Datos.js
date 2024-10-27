// src/Datos.js
import React, { useEffect, useState } from 'react';
import {
    fetchStores,
    fetchCustomers,
    fetchStaff,
    fetchInventory,
    rentMovie,
    makePayment
} from '../api';

const Datos = () => {
    const [stores, setStores] = useState([]);
    const [customers, setCustomers] = useState([]);
    const [staff, setStaff] = useState([]);
    const [inventory, setInventory] = useState([]);

    const [selectedStore, setSelectedStore] = useState('');
    const [selectedCustomer, setSelectedCustomer] = useState('');
    const [selectedStaff, setSelectedStaff] = useState('');
    const [selectedInventory, setSelectedInventory] = useState('');

    const [customerId, setCustomerId] = useState(null);
    const [staffId, setStaffId] = useState(null);
    const [inventoryId, setInventoryId] = useState(null);
    const [inventoryPrice, setInventoryPrice] = useState(0);
    const [rentalId, setRentalId] = useState(null);

    useEffect(() => {
        const loadStores = async () => {
            try {
                const data = await fetchStores();
                setStores(data);
            } catch (error) {
                console.error("Error fetching stores:", error);
            }
        };
        loadStores();
    }, []);

    const handleStoreChange = async (event) => {
        const storeId = event.target.value;
        setSelectedStore(storeId);
        
        if (storeId) {
            try {
                const [customersData, staffData, inventoryData] = await Promise.all([
                    fetchCustomers(storeId),
                    fetchStaff(storeId),
                    fetchInventory(storeId)
                ]);

                setCustomers(customersData);
                setStaff(staffData);
                setInventory(inventoryData);
            } catch (error) {
                console.error("Error fetching data for the selected store:", error);
            }
        }
    };

    const handleCustomerChange = (event) => {
        const selected = customers.find(c => c.customer_id === Number(event.target.value));
        setSelectedCustomer(event.target.value);
        setCustomerId(selected.customer_id);
    };

    const handleStaffChange = (event) => {
        const selected = staff.find(s => s.staff_id === Number(event.target.value));
        setSelectedStaff(event.target.value);
        setStaffId(selected.staff_id);
    };

    const handleInventoryChange = (event) => {
        const selected = inventory.find(i => i.inventory_id === Number(event.target.value));
        setSelectedInventory(event.target.value);
        setInventoryId(selected.inventory_id);
        setInventoryPrice(selected.replacement_cost);
    };

    const handleRentMovie = async () => {
        if (!inventoryId || !customerId || !staffId) {
            alert("Por favor, selecciona todos los campos antes de continuar.");
            return;
        }

        try {
            const rentalResponse = await rentMovie({
                inventory_id: inventoryId,
                customer_id: customerId,
                staff_id: staffId
            });

            setRentalId(rentalResponse.rental_id);
            alert(`Renta creada exitosamente! ID de Renta: ${rentalResponse.rental_id}`);

            // Realizar el pago
            const paymentResponse = await makePayment({
                rental_id: rentalResponse.rental_id,
                customer_id: customerId,
                staff_id: staffId,
                amount: inventoryPrice
            });

            alert(`Pago registrado exitosamente! ID de Pago: ${paymentResponse.payment_id}`);
        } catch (error) {
            console.error("Error durante la renta o el pago:", error);
            alert("Hubo un error al procesar la renta o el pago.");
        }
    };

    return (
        <div>
            <h1>Renta de Películas</h1>
            <div>
                <label>Tienda:</label>
                <select value={selectedStore} onChange={handleStoreChange}>
                    <option value="">Selecciona una tienda</option>
                    {stores.map(store => (
                        <option key={store.store_id} value={store.store_id}>
                            {store.store_id}
                        </option>
                    ))}
                </select>
            </div>
            <div>
                <label>Cliente:</label>
                <select value={selectedCustomer} onChange={handleCustomerChange}>
                    <option value="">Selecciona un cliente</option>
                    {customers.map(customer => (
                        <option key={customer.customer_id} value={customer.customer_id}>
                            {customer.first_name} {customer.last_name}
                        </option>
                    ))}
                </select>
            </div>
            <div>
                <label>Personal:</label>
                <select value={selectedStaff} onChange={handleStaffChange}>
                    <option value="">Selecciona un personal</option>
                    {staff.map(staffMember => (
                        <option key={staffMember.staff_id} value={staffMember.staff_id}>
                            {staffMember.first_name} {staffMember.last_name}
                        </option>
                    ))}
                </select>
            </div>
            <div>
                <label>Inventario:</label>
                <select value={selectedInventory} onChange={handleInventoryChange}>
                    <option value="">Selecciona un título</option>
                    {inventory.map(item => (
                        <option key={item.inventory_id} value={item.inventory_id}>
                            {item.film_title} - ${item.replacement_cost}
                        </option>
                    ))}
                </select>
            </div>
            <button onClick={handleRentMovie}>Crear Renta y Pago</button>
            <div>
                <h3>Resumen:</h3>
                <p>Cliente ID: {customerId}</p>
                <p>Personal ID: {staffId}</p>
                <p>Inventario ID: {inventoryId}</p>
                <p>Precio: ${inventoryPrice}</p>
                <p>ID de Renta: {rentalId}</p>
            </div>
        </div>
    );
};

export default Datos;
