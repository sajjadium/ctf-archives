import './App.css';
import * as React from 'react';
import { Routes, Route } from 'react-router-dom';

import {Header} from "./components";
import {LoginForm, RegisterForm,Home,Pay, Report} from "./endpoints";

function App() {
  return (
    <div className="App">
      <div className='bg-zinc-900 h-full'>
        <Routes>
          <Route path="/" element={<LoginForm />} />
          <Route path="register" element={<RegisterForm />} />
          <Route path="login" element={<LoginForm />} />
          <Route path="home" element={<Home />} />
          <Route path="pay" element={<Pay />} />
          <Route path="report" element={<Report />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
