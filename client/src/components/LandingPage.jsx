import React from 'react';
import './LandingPage.css'; // Make sure to create this CSS file

const LandingPage = ({ history }) => {
  return (
    <div className="landing-container">
      <div className="overlay">
        <header>
          <h1>Grandma's Recipe Box</h1>
          <nav>
            <button className="login-btn">Login</button>
            <button className="signup-btn">Sign Up</button>
          </nav>
        </header>
        <main>
          <div className="call-to-action">
            <h2>Find & Share Great Recipes with Ease</h2>
            <button className="start-cooking-btn" onClick={() => history.push('/login')}>Start Cooking!</button>
          </div>
        </main>
      </div>
    </div>
  );
};

export default LandingPage;
