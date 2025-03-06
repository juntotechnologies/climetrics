import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login = () => {
  const [activeTab, setActiveTab] = useState('login');
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    fullName: ''
  });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const endpoint = activeTab === 'login' ? '/api/auth/login' : '/api/auth/register';
      const response = await axios.post(endpoint, formData);
      
      if (activeTab === 'login') {
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('username', response.data.username);
        navigate('/dashboard');
      } else {
        setActiveTab('login');
        alert('Registration successful! Please login.');
      }
    } catch (error) {
      alert(error.response?.data?.message || 'An error occurred');
    }
  };

  return (
    <div className="login-container">
      <h1>Climetrics</h1>
      <div className="tabs">
        <button 
          className={activeTab === 'login' ? 'active' : ''} 
          onClick={() => setActiveTab('login')}
        >
          Login
        </button>
        <button 
          className={activeTab === 'register' ? 'active' : ''} 
          onClick={() => setActiveTab('register')}
        >
          Register
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={formData.username}
          onChange={(e) => setFormData({...formData, username: e.target.value})}
        />
        <input
          type="password"
          placeholder="Password"
          value={formData.password}
          onChange={(e) => setFormData({...formData, password: e.target.value})}
        />
        {activeTab === 'register' && (
          <input
            type="text"
            placeholder="Full Name"
            value={formData.fullName}
            onChange={(e) => setFormData({...formData, fullName: e.target.value})}
          />
        )}
        <button type="submit">
          {activeTab === 'login' ? 'Login' : 'Register'}
        </button>
      </form>
    </div>
  );
};

export default Login; 