import React, { Component } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';

class App extends Component {
  render() {
    return (
    <Router>
      <Switch>
        <Route path="/" exact component={LandingPage} />
        <Route path="/login" component={LoginPage} />
        <Route path="/register" component={RegisterPage}/>
        {/* Other routes */}
      </Switch>
    </Router>
    );
  }
}

export default App;