import React from 'react'
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css';
import Home from './components/pages/Home';
import About from './components/pages/About';
import Model from './components/pages/Model';


function App() {
  return (
    <div className="App">
      <Router>
        <Navbar />
        <Routes>
          <Route path='/' exact element = {< Home />} />
          <Route path='/about' exact element = {< About />} />
          <Route path='/model' exact element = {< Model />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
