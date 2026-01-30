import React, { useEffect, useState } from 'react';
import { getSummary, uploadFile, downloadReport } from '../api';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import Navbar from './Navbar';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const Dashboard = () => {
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchSummary = async () => {
        try {
            const { data } = await getSummary();
            setSummary(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchSummary();
    }, []);

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            await uploadFile(formData);
            fetchSummary();
            alert('File uploaded successfully!');
        } catch (error) {
            alert('Upload failed: ' + (error.response?.data?.error || 'Unknown error'));
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <Navbar />
            <div className="container">
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
                    <div>
                        <input type="file" onChange={handleFileUpload} id="file-upload" style={{ display: 'none' }} />
                        <label htmlFor="file-upload" className="btn btn-primary">Upload CSV</label>
                    </div>
                    <button className="btn btn-primary" onClick={downloadReport}>Download Report (PDF)</button>
                </div>

                {summary ? (
                    <div className="grid">
                        <div className="card">
                            <h3>Latest Dataset Summary</h3>
                            <div className="stat-item">File: <b>{summary.file_name}</b></div>
                            <div className="stat-item">Total Equipment: <b>{summary.total_count}</b></div>
                            <div className="stat-item">Avg Flowrate: <b>{summary.avg_flowrate}</b></div>
                            <div className="stat-item">Avg Pressure: <b>{summary.avg_pressure}</b></div>
                            <div className="stat-item">Avg Temperature: <b>{summary.avg_temperature}</b></div>
                        </div>

                        <div className="card">
                            <h3>Average Metrics</h3>
                            <Bar
                                data={{
                                    labels: ['Flowrate', 'Pressure', 'Temperature'],
                                    datasets: [{
                                        label: 'Average Values',
                                        data: [summary.avg_flowrate, summary.avg_pressure, summary.avg_temperature],
                                        backgroundColor: ['#3b82f6', '#ef4444', '#10b981'],
                                    }]
                                }}
                            />
                        </div>

                        <div className="card">
                            <h3>Equipment Types</h3>
                            <div style={{ height: '300px', display: 'flex', justifyContent: 'center' }}>
                                <Pie
                                    data={{
                                        labels: Object.keys(summary.type_distribution),
                                        datasets: [{
                                            data: Object.values(summary.type_distribution),
                                            backgroundColor: ['#6366f1', '#ec4899', '#f59e0b', '#10b981', '#3b82f6'],
                                        }]
                                    }}
                                />
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="card"><h3>No data available. Upload a CSV to get started.</h3></div>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
