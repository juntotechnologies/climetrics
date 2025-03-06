import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import './styles/App.css';

function App() {
  const isAuthenticated = !!localStorage.getItem('token');

  return (
    <Router>
      <div className="app">
        <Routes>
          <Route 
            path="/" 
            element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login />} 
          />
          <Route 
            path="/dashboard" 
            element={isAuthenticated ? <Dashboard /> : <Navigate to="/" />} 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 