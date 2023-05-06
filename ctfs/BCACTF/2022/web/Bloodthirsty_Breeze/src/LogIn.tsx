import React, { useState } from 'react';
import './App.css';
import Button from 'react-bootstrap/Button';
import { Collapse, Form } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

function LogIn() {
    const navigator = useNavigate();

    const [invalidUnamePass, setInvalidUnamePass] = useState(false);
  

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.stopPropagation();
        event.preventDefault();

        const target = event.target as typeof event.target & {
            username: { value: string };
            password: { value: string };
        };

        const body = JSON.stringify({
            username: target.username.value,
            password: target.password.value,
        });

        fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body,
        }).then(response => {
            if (response.ok) navigator("/menu");
            else if (response.status >= 500) alert("Internal Server Error!");
            else setInvalidUnamePass(true);
        });
    };

    return (
        <div className="justify-content-center align-items-center bg-dark bg-gradient text-white vstack" style={{ width: "100vw", height: "100vh" }}>
            <Form className="justify-content-center align-items-center col-md-5" onSubmit={handleSubmit}>
                <Form.Group className="mb-4" controlId="username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control type="username" placeholder="Username" required={true} />
                </Form.Group>
                <Form.Group className="mb-4" controlId="password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Password" required={true} />
                </Form.Group>
                <Collapse in={invalidUnamePass}><p>Invalid username or password</p></Collapse>
                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
        </div>
    );
}

export default LogIn;
