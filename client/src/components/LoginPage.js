import React, { useState } from 'react';
import './LoginPage.css'; // You will create this CSS file based on style.css

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (event) => {
    event.preventDefault();
    // Here you would handle the login logic, possibly sending a request to your Flask API
    console.log('Login with:', username, password);
  };

  return (
    <div className="container">
      <form onSubmit={handleLogin}>
        <h2>Login</h2>
        <div>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            size="20"
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            size="20"
          />
        </div>
        <button type="submit">Login</button>
      </form>
      <p>Don't have an account? We got you! <a href="/register">Sign up here</a>.</p>
    </div>
  );
};

export default LoginPage;
