import * as bcrypt from "bcrypt";
import { v4 as uuid } from "uuid";
import { UnknownRequest } from "@zensors/expedite";

import { query } from "./database";
import { SafeError } from "../utils";

query`
    CREATE TABLE IF NOT EXISTS user_auth (
        username text PRIMARY KEY,
        password_hash text NOT NULL
    );
`;
query`
    CREATE TABLE IF NOT EXISTS user_token (
        token text PRIMARY KEY,
        username text NOT NULL REFERENCES user_auth (username)
    );
`;


export interface UserAuth {
    username: string;
    password_hash: string;
}

export interface UserToken {
    username: string;
    token: string;
}

const getUser = async (username: string) => {
    const user = await query<UserAuth>`
        SELECT username, password_hash
        FROM user_auth
        WHERE username = ${username};
    `;

    if (user.length === 1) {
        return user[0];
    }
}

const generateToken = async (username: string) => {
    const token = uuid();
    await query`
        INSERT INTO user_token (token, username)
        VALUES (${token}, ${username});
    `;
    return token;
}

export const register = async (username: string, password: string) => {
    if (!username.match(/^[a-zA-Z0-9_\-]{3,}$/)) {
        throw new SafeError(400, "Invalid username");
    }

    if (await getUser(username)) {
        throw new SafeError(400, "User already exists");
    }

    const hashedPassword = await bcrypt.hash(password, 14);

    await query`
        INSERT INTO user_auth (username, password_hash)
        VALUES (${username}, ${hashedPassword});
    `;

    return generateToken(username);
};

export const login = async (username: string, password: string) => {
    const user = await getUser(username);
    if (!user) {
        throw new SafeError(401, "Bad credentials");
    }

    const result = await bcrypt.compare(password, user.password_hash);
    if (!result) {
        throw new SafeError(401, "Bad credentials");
    }

    return generateToken(user.username);
}

export const requireLogin = async <T extends UnknownRequest>(req: T) => {
    const userToken = req.cookies["user_token"];
    if (typeof userToken !== "string") {
        throw new SafeError(401, "Unauthorized");
    }

    const usernames = await query<UserToken>`
        SELECT token, username
        FROM user_token
        WHERE token = ${userToken};
    `;

    if (usernames.length !== 1) {
        throw new SafeError(401, "Unauthorized");
    }

    const { username } = usernames[0];
    const user = await getUser(username);

    if (!user) {
        throw new SafeError(401, "Unauthorized");
    }

    return Object.assign(req, { user });
}
