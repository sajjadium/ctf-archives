import * as React from "react";
import { api } from "../../client";

import { navigate } from "../../history";
import { UserContext } from "../../providers/user-provider";

import "./index.scss";

export interface Props { }

export const Header = (props: Props) => {
    const { user, refresh } = React.useContext(UserContext);

    return (
        <div className="header">
            <div className="title" onClick={() => navigate("/")}>
                <div className="wowza">Wowza!</div>
                <div className="console">Search Console</div>
            </div>
            <div className="auth">
                {
                    user.value ? <div onClick={async () => { await api.auth.logout(); refresh(); navigate("/"); }}>Logout</div> :
                    <>
                        <div onClick={() => { refresh(); navigate("/login") }}>Login</div>
                        <div onClick={() => { refresh(); navigate("/register") }}>Register</div>
                    </>
                }
            </div>
        </div>
    )
}