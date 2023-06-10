import './App.css';
import * as React from 'react';
import { Routes, Route } from 'react-router-dom';

import {Header} from "./components";
import {LoginForm, RegisterForm,Home,Shop,Items, Checkout} from "./endpoints";

function App() {
  return (
    <div className="App">
      <div className='bg-slate-900 h-full'>
        <Routes>
          <Route path="/" element={<LoginForm />} />
          <Route path="register" element={<RegisterForm />} />
          <Route path="login" element={<LoginForm />} />
          <Route path="home" element={<Home />} />
          <Route path="shop" element={<Shop />} />
          <Route path="items" element={<Items />} />
          <Route path="checkout" element={<Checkout />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
