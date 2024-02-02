import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { Routes, Route } from 'react-router-dom';

import Index from './pages/Index';
import Register from './pages/Register';
import Login from './pages/Login';
import Home from './pages/Home';
import View from './pages/View';

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <div className="container mt-5">
      <div>
        <h2>🔥 burnbin</h2>
        <p>The most secure place to create and store private pastes that can only be read once.</p>
      </div>
      <hr />
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/view/:id" element={<View />} />
        <Route path="*" element={
          <h3>404 page not found</h3>
        }/>
      </Routes>
    </div>
  </BrowserRouter>
);