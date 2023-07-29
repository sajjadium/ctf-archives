import crypto from "crypto";
import db from "@/utils/db";
import { compare } from "bcryptjs";
import { getUserByUsername } from "@/utils/helpers";

export default async function handler(req, res) {
    if (req.method !== "POST") {
        res.status(405).json({ msg: "Method not allowed" });
        return;
    }

    const { username, password } = req.body;

    if (!username || !password) {
        res.status(400).json({ msg: "Please provide all fields" });
        return;
    }

    const user = await getUserByUsername(username);

    if (user && (await compare(password, user.password))) {
        const cookie = crypto.randomBytes(32).toString("hex");
        await new Promise((resolve, reject) => {
            const sql = "UPDATE users SET session = ? WHERE username = ?";
            db.run(sql, [cookie, username], (err) => {
                if (err) {
                    reject(err);
                }
                resolve();
            });
        });
        res.statusCode = 200;
        res.setHeader("Set-Cookie", `session=${cookie}; Path=/; HttpOnly; SameSite=Strict`);
        res.json({ msg: "Welcome back!"});
        res.end();
    } else {
        res.status(403).json({ msg: "Password incorrect" });
        return;
    }
}
