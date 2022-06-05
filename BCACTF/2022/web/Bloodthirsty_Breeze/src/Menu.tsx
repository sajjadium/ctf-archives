import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { MenuItem } from "../api/src/MenuItem";
import "./Menu.css";

function Menu() {
    const navigator = useNavigate();

    const [data, setData] = useState<MenuItem[]>();


    useEffect(() => {(async () => {
        let response = await fetch("/api/menu");
        if (response.ok) {
            setData(await response.json());
        } else if (response.status === 403) navigator("/log-in");
        else navigator("/");
    })()}, [navigator]);

    return (
        <div className="align-items-center bg-dark bg-gradient text-white vstack" style={{ width: "100vw", height: "100vh", overflow: "scroll"}}>
            <h1 style={{ fontFamily: "cursive", paddingTop: "2rem", }}>Menu:</h1>
            {
                data?.map(
                    item => <div className="menu-item">
                        <div className="left-menu-block">
                            <img src={item.imageURL} style={{maxWidth: "20vw", maxHeight: "20rem"}} alt="the menu item"/>
                        </div><div className="right-menu-block">
                            <span>{item.name}</span>
                            <details>
                                <summary>More details</summary>
                                <div>{item.description}</div>
                            </details>
                        </div>
                    </div>
                ) ?? <p>Loading your Bloodthirsty Breeze menu...</p>
            }
        </div>
    );
}

export default Menu;
