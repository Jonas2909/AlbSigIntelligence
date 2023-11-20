import './App.css';

import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './Login';
import Visualization from './Visualization';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/Visualization" element={<Visualization />} />
        <Route path="/" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

export default App;
