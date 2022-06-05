import React from 'react';
import './App.css';
import { Route, Routes } from 'react-router-dom';
import Home from "./Home";
import LogIn from './LogIn';
import SignUp from './SignUp';
import Menu from './Menu';

function App() {
    return (
        <Routes>
            <Route path="/" element={<Home/>}/>
            <Route path="/log-in" element={<LogIn/>}/>
            <Route path="/sign-up" element={<SignUp/>}/>
            <Route path="/menu" element={<Menu/>}/>
        </Routes>
    );
}

export default App;
