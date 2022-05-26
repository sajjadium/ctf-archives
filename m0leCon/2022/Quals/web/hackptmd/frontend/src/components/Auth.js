import { useNavigate, Navigate } from "react-router-dom";
import { useState } from "react";

import { Message } from './Message';

function Login({ CSRFToken }) {

    const [error, setError] = useState(undefined);

    const navigate = useNavigate()
    const goToHome = () => navigate('/');

    const submitLogin = async (e) => {
        e.preventDefault()
        const username = document.getElementById('username').value
        const password = document.getElementById('password').value

        const r = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, _csrf: CSRFToken })
        })

        if (r.status !== 200) {
            const j = await r.json()
            setError(j.error || "Login failed")
        } else {
            goToHome()
        }
    }

    return <>
        <Message msg={error} type='error' />

        <p className="h2 text-center my-4 pb-3">Login</p>

        <form className="mx-auto col-xl-3 col-lg-5 col-md-6 col-sm-8" onSubmit={submitLogin}>
            <div class="mb-3">
                <input type="text" class="form-control" id="username" placeholder="username" />
            </div>
            <div class="mb-3">
                <input type="password" class="form-control" id="password" placeholder="password" minLength="6" />
            </div>
            <button type="submit" class="btn btn-primary mx-auto" id="submit" style={{ display: 'block', width: '100%' }}>Login</button>
        </form>
    </>
}

function Signup({ CSRFToken }) {

    const [error, setError] = useState(undefined);

    const navigate = useNavigate()
    const goToLogin = () => navigate('/login');

    const submitSignup = async (e) => {
        e.preventDefault()
        const username = document.getElementById('username').value
        const password = document.getElementById('password').value

        const r = await fetch('/api/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, _csrf: CSRFToken })
        })

        if (r.status !== 200) {
            const j = await r.json()
            setError(j.error || "Signup failed")
        } else {
            goToLogin()
        }
    }

    return <>
        <Message msg={error} type='error' />

        <p className="h2 text-center my-4 pb-3">Signup</p>

        <form className="mx-auto col-xl-3 col-lg-5 col-md-6 col-sm-8" onSubmit={submitSignup}>
            <div class="mb-3">
                <input type="text" class="form-control" id="username" placeholder="username" />
            </div>
            <div class="mb-3">
                <input type="password" class="form-control" id="password" placeholder="password" minLength="6" />
            </div>
            <button type="submit" class="btn btn-primary mx-auto" id="submit" style={{ display: 'block', width: '100%' }}>Signup</button>
        </form>
    </>
}


function Logout() {

    fetch('/api/logout')

    return <Navigate to="/" />

}

export { Login, Signup, Logout }