import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [selectedService, setSelectedService] = useState('all');

  useEffect(() => {
    fetchMetrics();
  }, [selectedService]);

  const fetchMetrics = async () => {
    try {
      const response = await axios.get(`/api/metrics?service=${selectedService}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setMetrics(response.data);
    } catch (error) {
      console.error('Error fetching metrics:', error);
    }
  };

  return (
    <div className="dashboard">
      <h1>Surgical Metrics Dashboard</h1>
      
      <select 
        value={selectedService} 
        onChange={(e) => setSelectedService(e.target.value)}
      >
        <option value="all">All Services</option>
        <option value="Melanoma">Melanoma</option>
        <option value="Gastrectomy">Gastrectomy</option>
        <option value="Whipple">Whipple</option>
      </select>

      {metrics && (
        <div className="metrics-grid">
          <div className="metric-card">
            <h3>Length of Stay</h3>
            <LineChart width={500} height={300} data={metrics.losData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="los" stroke="#8884d8" />
            </LineChart>
          </div>
          
          {/* Add more metric cards here */}
        </div>
      )}
    </div>
  );
};

export default Dashboard; 