import React from 'react';
import './App.css';
import Button from 'react-bootstrap/Button';
import { Stack } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

function Home() {
    const navigator = useNavigate();

    return (
        <Stack gap={2} className="col-md-5 justify-content-center align-items-center bg-dark bg-gradient text-white" style={{ width: "100vw", height: "100vh" }}>
            <h1>Welcome to <i>Bloodthirsty Breeze</i>! 🧛‍♀️</h1>
            <h2>Your one-stop shop for all your bloody needs!</h2>
            <Button variant="light" style={{ width: "20rem"}} onClick={() => navigator("/log-in" )}>Log In</Button>
            <Button variant="info"  style={{ width: "20rem"}} onClick={() => navigator("/sign-up")}>Sign Up</Button>
        </Stack>
    );
}

export default Home;
