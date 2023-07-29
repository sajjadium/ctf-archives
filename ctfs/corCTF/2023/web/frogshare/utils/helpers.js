import cookie from "cookie";

import db from "./db";

export const getUserBySession = async (session) => {
    return await new Promise((resolve, reject) => {
        db.get(
            "SELECT * FROM users WHERE session = ?",
            [session],
            (err, row) => {
                if (err) {
                    reject(err);
                }
                resolve(row ? row : null);
            }
        );
    });
};

export const getUserByUsername = async (username) => {
    return await new Promise((resolve, reject) => {
        const sql = "SELECT * FROM users WHERE username = ?";
        db.get(sql, [username], (err, row) => {
            if (err) {
                reject(err);
            }
            resolve(row);
        });
    });
};

export const getFrogs = async () => {
    return await new Promise((resolve, reject) => {
        db.all(
            "SELECT f.*, u.username AS creator FROM frogs AS f JOIN users AS u ON f.creator = u.id WHERE f.is_approved = 1;",
            [],
            (err, rows) => {
                if (err) {
                    reject(err);
                }
                resolve(rows);
            }
        );
    });
};

export const getFrogById = async (frogId, username, isAdmin) => {
    return await new Promise((resolve, reject) => {
        db.get(
            "SELECT f.*, u.username AS creator FROM frogs AS f JOIN users AS u ON f.creator = u.id WHERE f.id = ?",
            [frogId],
            (err, row) => {
                if (err) {
                    reject(err);
                }
                if (row) {
                    if (isAdmin || username === row.creator) {
                        resolve(row);
                    } else {
                        resolve(null);
                    }
                } else {
                    resolve(null);
                }
            }
        );
    });
};

export const getSessionCookie = (req) => {
    const cookieHeader = req?.headers?.cookie;
    return cookieHeader ? cookie.parse(cookieHeader)?.session : null;
};

export const isAuthenticated = async (req) => {
    const cookie = getSessionCookie(req);
    if (!cookie) return false;
    return !!(await getUserBySession(cookie));
};
