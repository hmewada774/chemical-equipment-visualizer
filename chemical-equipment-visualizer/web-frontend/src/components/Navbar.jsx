import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigate('/');
    };

    return (
        <nav className="nav">
            <h1 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--primary)' }}>
                ChemViz
            </h1>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                <Link to="/dashboard" style={{ textDecoration: 'none', color: 'var(--text)' }}>Dashboard</Link>
                <Link to="/history" style={{ textDecoration: 'none', color: 'var(--text)' }}>History</Link>
                <button onClick={handleLogout} className="btn" style={{ background: '#e2e8f0' }}>Logout</button>
            </div>
        </nav>
    );
};

export default Navbar;
