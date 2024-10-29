import axios from 'axios';

const API_URL = 'http://ec2-44-203-39-10.compute-1.amazonaws.com:5000';

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

export const rentMovie = async (data) => {
    const response = await axios.post(`${API_URL}/rent`, data);
    return response.data;
};

export const makePayment = async (data) => {
    const response = await axios.post(`${API_URL}/pay`, data);
    return response.data;
};
