import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
// Import the App component
import App from './App';

// Render the App component
ReactDOM.render(<App />, document.getElementById('root'));

fetch('/api/data')
  .then(response => response.json())
  .then(data => console.log(data));

  fetch('/api/getData')
  .then(response => response.json())
  .then(data => this.setState({ data }));
