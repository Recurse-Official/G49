// frontend/src/components/Leaderboard.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Leaderboard = () => {
    const [leaderboard, setLeaderboard] = useState([]);

    const fetchLeaderboard = async () => {
        try {
            const res = await axios.get('http://localhost:5000/leaderboard/get_leaderboard', {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            });
            setLeaderboard(res.data);
        } catch (err) {
            console.error(err);
            alert('Failed to fetch leaderboard');
        }
    }

    useEffect(() => {
        fetchLeaderboard();
    }, []);

    return (
        <div>
            <h2>Leaderboard</h2>
            <ol>
                {leaderboard.map((user, index) => (
                    <li key={index}>{user.username} - {user.points} points</li>
                ))}
            </ol>
        </div>
    );
}

export default Leaderboard;
