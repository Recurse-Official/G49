// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
// Import other components

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login" component={Login}/>
                <Route path="/register" component={Register}/>
                <Route path="/dashboard" component={Dashboard}/>
                {/* Add other routes */}
            </Routes>
        </Router>
    );
}

export default App;

