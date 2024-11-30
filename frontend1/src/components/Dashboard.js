// frontend/src/components/Dashboard.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [offers, setOffers] = useState([]);

    const fetchOffers = async (brand) => {
        try {
            const res = await axios.get(`http://localhost:5000/offers/get_offers?brand=${brand}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            });
            setOffers(res.data);
        } catch (err) {
            console.error(err);
            alert('Failed to fetch offers');
        }
    }

    useEffect(() => {
        // Example: Fetch offers for 'Zomato'
        fetchOffers('Zomato');
    }, []);

    return (
        <div>
            <h2>Offers</h2>
            <ul>
                {offers.map((offer, index) => (
                    <li key={index}>{offer.description}</li>
                ))}
            </ul>
        </div>
    );
}

export default Dashboard;
