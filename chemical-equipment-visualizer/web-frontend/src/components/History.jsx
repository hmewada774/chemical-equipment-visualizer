import React, { useEffect, useState } from 'react';
import { getHistory } from '../api';
import Navbar from './Navbar';

const History = () => {
    const [history, setHistory] = useState([]);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const { data } = await getHistory();
                setHistory(data);
            } catch (error) {
                console.error(error);
            }
        };
        fetchHistory();
    }, []);

    return (
        <div>
            <Navbar />
            <div className="container">
                <div className="card">
                    <h2>Upload History (Last 5)</h2>
                    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
                        <thead>
                            <tr style={{ textAlign: 'left', borderBottom: '1px solid #e2e8f0' }}>
                                <th style={{ padding: '1rem' }}>File Name</th>
                                <th style={{ padding: '1rem' }}>Uploaded At</th>
                                <th style={{ padding: '1rem' }}>Total Count</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((item) => (
                                <tr key={item.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                                    <td style={{ padding: '1rem' }}>{item.file_name}</td>
                                    <td style={{ padding: '1rem' }}>{new Date(item.uploaded_at).toLocaleString()}</td>
                                    <td style={{ padding: '1rem' }}>{item.total_count}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default History;
