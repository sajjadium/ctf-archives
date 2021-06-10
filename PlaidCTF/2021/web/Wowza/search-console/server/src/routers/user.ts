import { Router } from "@zensors/expedite";

import { User } from "../state";

export const userRouter =
    (new Router())
    .then(User.requireLogin);

userRouter.get("/")
    .return(({ user: { username }}) => ({ username }));