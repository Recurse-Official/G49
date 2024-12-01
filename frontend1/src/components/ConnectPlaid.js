// frontend/src/components/ConnectPlaid.js
import React, { useEffect } from 'react';
import axios from 'axios';

const ConnectPlaid = () => {
    const handleConnect = async () => {
        const response = await axios.post('http://localhost:5000/plaid/create_link_token', {}, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`
            }
        });
        const { link_token } = response.data;

        const handler = window.Plaid.create({
            token: link_token,
            onSuccess: async (public_token, metadata) => {
                // Send public_token to backend
                await axios.post('http://localhost:5000/plaid/exchange_public_token', { public_token }, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    }
                });
                alert('Plaid connected successfully!');
            },
            onExit: (err, metadata) => {
                if (err) {
                    console.error(err);
                }
            },
        });

        handler.open();
    };

    return (
        <button onClick={handleConnect}>Connect Bank Account</button>
    );
}

export default ConnectPlaid;
