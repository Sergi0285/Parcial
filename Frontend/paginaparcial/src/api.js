import axios from 'axios';

const API_URL = 'http://ec2-44-202-138-248.compute-1.amazonaws.com:5000';

export const rentMovie = (data) => axios.post(`${API_URL}/rent`, data);
export const makePayment = (data) => axios.post(`${API_URL}/pay`, data);
export const getRecentRentals = () => axios.get(`${API_URL}/recent_rentals`);
