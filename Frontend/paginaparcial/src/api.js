import axios from 'axios';

const API_URL = 'http://ec2-54-175-7-193.compute-1.amazonaws.com:5000';

export const rentMovie = async (data) => {
    const response = await fetch(`${API_URL}/rent`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al rentar la película');
    }

    return await response.json();
};

export const makePayment = async (data) => {
    const response = await fetch(`${API_URL}/pay`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al realizar el pago');
    }

    return await response.json();
};

export const getRecentRentals = async () => {
    const response = await fetch(`${API_URL}/recent_rentals`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al obtener las rentas');
    }

    return await response.json();
};

export const fetchStores = async () => {
    const response = await axios.get(`${API_URL}/stores`);
    return response.data;
};

export const fetchCustomers = async (storeId) => {
    const response = await axios.get(`${API_URL}/customers/${storeId}`);
    return response.data;
};

export const fetchStaff = async (storeId) => {
    const response = await axios.get(`${API_URL}/staff/${storeId}`);
    return response.data;
};

export const fetchInventory = async (storeId) => {
    const response = await axios.get(`${API_URL}/inventory/${storeId}`);
    return response.data;
};
