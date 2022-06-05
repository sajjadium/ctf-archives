import React from 'react';
import './App.css';
import './SignUp.css';

function SignUp() {
    return (
        <div className="justify-content-center align-items-center bg-dark bg-gradient text-white vstack" style={{ width: "100vw", height: "100vh" }}>
            <div id="construction-sign">
                <div>
                    <div className="screw upper right"></div>
                    <div className="screw lower right"></div>
                    <div className="screw upper leftt"></div>
                    <div className="screw lower leftt"></div>
                    <span>This site is under construction.</span><br/>
                    <span className="smaller">Come back in {(Math.floor(Math.random() * 2000394) + 1).toLocaleString()} days!</span>
                </div>
            </div>
        </div>
    );
}

export default SignUp;