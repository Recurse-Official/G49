// frontend/src/components/Scanner.js
// frontend/src/components/Scanner.js
import React, { useState } from 'react';
import QrScanner from 'react-qr-scanner';
import axios from 'axios';

const Scanner = () => {
    const [scanResult, setScanResult] = useState('');

    const handleScan = async data => {
        if (data) {
            setScanResult(data.text); // `react-qr-scanner` provides `text` property for scanned data
            try {
                const res = await axios.post('http://localhost:5000/transactions/scan', {
                    scanned_data: data.text
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
    };

    const handleError = err => {
        console.error(err);
    };

    const previewStyle = {
        height: 240,
        width: 320,
    };

    return (
        <div>
            <h2>Scan Transaction</h2>
            <QrScanner
                delay={300}
                style={previewStyle}
                onError={handleError}
                onScan={handleScan}
            />
            <p>{scanResult}</p>
        </div>
    );
};

export default Scanner;

