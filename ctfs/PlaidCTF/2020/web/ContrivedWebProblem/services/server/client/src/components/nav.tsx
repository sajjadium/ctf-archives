import * as React from "react";

import { useHistory } from "../utils/utils";
import { UserContext } from "../contexts/user";

import "./nav.scss";

const NavButton = ({ text, path }: { text: string, path: string }) => {
    const history = useHistory();

    return <input type="button" className="pure-button btn btn-large red waves-effect waves-light" onClick={() => history.push(path)} value={text}/>;
}

export default () => {
    const { data: user } = React.useContext(UserContext);

    let extraButtons = [
        <NavButton key="home" text="Home" path="/"/>,
        <NavButton key="profile" text="Profile" path="/profile"/>,
    ]

    return (
        <div className="nav">
            {
                user !== null && user.kind !== "none"
                    ? extraButtons
                    : []
            }
            <NavButton text="Login" path="/login"/>
            <NavButton text="Register" path="/register"/>
        </div>
    )
}