import * as React from "react";

import { Button, Input, Frame } from "react-pwn";
import { toast } from "react-toastify";
import { api } from "../../client";
import { navigate } from "../../history";
import { UserContext } from "../../providers/user-provider";

export interface Props {}

export const Register = (props: Props) => {
    const { refresh } = React.useContext(UserContext);

    const [username, setUsername] = React.useState("");
    const [password, setPassword] = React.useState("");

    const onSubmit = async () => {
        if (!username || !password) return;

        try {
            await api.auth.register(username, password);
            refresh();
            navigate("/");
        } catch (e) {
            toast.error(e);
        }
    }

    return (
        <Frame
            className="login"

        >
            <div className="title">Register</div>
            <Input
                value={username}
                onChange={setUsername}
                placeholder={"Username"}
                onEnter={onSubmit}
            />
            <Input
                type={"password"}
                value={password}
                onChange={setPassword}
                placeholder={"Password"}
                onEnter={onSubmit}
            />
            <Button
                label={"Register"}
                onClick={onSubmit}
            />
        </Frame>
    )
}