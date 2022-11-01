import { Router, helpers } from "https://deno.land/x/oak@v11.1.0/mod.ts";
import Food from './db.js';


const apiRouter = new Router({prefix: "/api"});

// Check if user is logged in
apiRouter.use(async (ctx, next) => {
    if (await ctx.cookies.get('admin') === '1') {
        await next();
    } else {
        await ctx.response.redirect("/login");
    }
});


apiRouter.get("/", (ctx) => {
    ctx.response.body = 'Food API get by id: /api/food/<int>';
});


apiRouter.get("/food/:id", async(ctx) => {
    const id = helpers.getQuery(ctx, { mergeParams: true });
    try {
        const res = await Food.select({id: 'id', name: 'name'}).where(id).all()
        ctx.response.body = res;
    }
    catch (e) {
        ctx.response.body = e.name
    }
});


export default apiRouter;