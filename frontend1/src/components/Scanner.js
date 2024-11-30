// frontend/src/components/Scanner.js
import React, { useState } from 'react';
import QrReader from 'react-qr-reader';
import axios from 'axios';

const Scanner = () => {
    const [scanResult, setScanResult] = useState('');

    const handleScan = async data => {
        if (data) {
            setScanResult(data);
            // Assuming data contains transaction info like amount
            // Here, you can send it to backend to check budget
            try {
                const res = await axios.post('http://localhost:5000/transactions/scan', {
                    scanned_data: data
                }, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`
                    }
                });
                // Handle response (utility/non-utility, warnings)
                alert(JSON.stringify(res.data));
            } catch (err) {
                console.error(err);
                alert('Error processing scanned data');
            }
        }
    }

    const handleError = err => {
        console.error(err);
    }

    return (
        <div>
            <h2>Scan Transaction</h2>
            <QrReader
                delay={300}
                onError={handleError}
                onScan={handleScan}
                style={{ width: '100%' }}
            />
            <p>{scanResult}</p>
        </div>
    );
}

export default Scanner;
