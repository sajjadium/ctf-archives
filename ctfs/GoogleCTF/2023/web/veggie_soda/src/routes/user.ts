// @ts-ignore  
import { Router, Context } from 'https://deno.land/x/oak/mod.ts';

import User from '../models/classes/User.ts';
import { AppState } from '../utils/session.ts';

const router = new Router<AppState>();


router.get('/profile', async (ctx: Context) => {
    var username = await ctx.state.session.get('username');
    const verifyUser = await ctx.state.users.hasUser(username);

    if (!username || !verifyUser){
        ctx.response.redirect('/');
        return;
    }
    const csrf = await ctx.state.session.get("csrf");
    const u = await ctx.state.users.getUser(username) as User;

    let posts = [...u.posts.entries()].reduce((obj, [key, value]) => (obj[key] = value["content"], obj), {});
    let sodas = [...u.sodas.entries()].reduce((obj, [key, value]) => (obj[key] = value["note"], obj), {});
    ctx.render("./views/profile.ejs", {data: {username: u.getUsername(), csrf_token: csrf},
        sodas: sodas, posts: posts});
});

export default router;
