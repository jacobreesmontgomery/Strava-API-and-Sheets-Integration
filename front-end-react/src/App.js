import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Components/Home/Home.tsx';
import BasicStats from './Components/BasicStats/BasicStats.tsx';
import Database from './Components/Database/Database.tsx';
import Navbar from './Components/Navbar/Navbar.tsx';
import './App.css';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/basic-stats" element={<BasicStats />} />
        <Route path="/database" element={<Database />} />
      </Routes>
    </Router>
  );
};

export default App;
