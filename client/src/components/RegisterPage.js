import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import './RegisterPage.css'; // Make sure to create this CSS file

function RegisterPage() {
  let history = useHistory();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    // Here you would typically make an API call to your backend to register the user
    console.log('Register with:', username, password);
    // On successful registration, redirect to the login page
    history.push('/login');
  };

  return (
    <div className="register-container">
      <form onSubmit={handleSubmit}>
        <h2>Sign Up</h2>
        <input 
          type="text" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
          placeholder="Username" 
          required 
        />
        <input 
          type="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          placeholder="Password" 
          required 
        />
        <button type="submit">Register</button>
      </form>
      <p>Already have an account? <a href="/login">Login here</a>.</p>
    </div>
  );
}

export default RegisterPage;
