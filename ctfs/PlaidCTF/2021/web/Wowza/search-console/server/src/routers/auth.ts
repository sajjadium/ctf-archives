import { marshalBody, Router } from "@zensors/expedite";
import { M } from "@zensors/sheriff";

import { User } from "../state";

// Users are for site admininistrators
export const authRouter = new Router();

authRouter.post("/login")
    .then(marshalBody(M.obj({ username: M.str, password: M.str })))
    .finish(async (req, res) => {
        const token = await User.login(req.body.username, req.body.password);
        res.cookie("user_token", token, { httpOnly: true, });
        res.json({ });
    });

authRouter.post("/register")
    .then(marshalBody(M.obj({ username: M.str, password: M.str })))
    .finish(async (req, res) => {
        const token = await User.register(req.body.username, req.body.password);
        res.cookie("user_token", token, { httpOnly: true });
        res.json({ });
    });

authRouter.post("/logout")
    .finish(async (req, res) => {
        res.clearCookie("user_token");
        res.json({});
    })