import * as React from "react";

import { UserContext } from "../contexts/user";

import { rest } from "../actions/rest";
import { useHistory } from "../utils/utils";

import "./login.scss";

export default (props: { register?: true }) => {
    const [email, setEmail] = React.useState("");
    const [password, setPassword] = React.useState("");
    const [name, setName] = React.useState("");
    const { refresh } = React.useContext(UserContext);
    const history = useHistory();

    const submit = async () => {
        if (props.register) {
            await rest("register", [], { email, password, name });
        } else {
            await rest("login", [], { email, password });
        }
        refresh();
        history.push("/");
    }

    return (
        <div className="login pure-form pure-form-stacked">
            <h1>{ props.register ? "Register" : "Login" }</h1>
            <div className="form pure-form pure-form-stacked">
                {
                    props.register
                        ? (
                            <input
                                className="name"
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                placeholder="Your Name"
                            />
                        ) : undefined
                }
                <input
                    className="email"
                    type="text"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email Address"
                />
                <input
                    className="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                />
            </div>
            <input type="button" className="submit pure-button large-btn btn teal" onClick={submit} value="Submit" />
        </div>
    );
}