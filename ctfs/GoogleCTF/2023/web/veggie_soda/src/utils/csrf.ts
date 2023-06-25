// @ts-ignore  
import { computeHmacTokenPair, computeVerifyHmacTokenPair } from "https://deno.land/x/deno_csrf@0.0.4/mod.ts"
// @ts-ignore  
import { Context, Middleware, Status } from 'https://deno.land/x/oak/mod.ts';
// @ts-ignore 
import { Session } from "https://deno.land/x/oak_sessions/mod.ts";

const getCsrfMiddleware = async function (ctx: Context, key: string): Promise<boolean>{
    if (ctx.request.url.searchParams.size) {
        const cookies_token = await ctx.cookies.get("token");
        const csrf = ctx.request.url.searchParams.get("csrf");
        
        if (!csrf || !cookies_token || !computeVerifyHmacTokenPair(key, csrf, cookies_token)){
            return false;
        }        
        return true;
    }

    const HMACpair = computeHmacTokenPair(key, 300);
    await ctx.state.session.set("csrf", HMACpair.tokenStr);
    await ctx.cookies.set("token", HMACpair.cookieStr);
    return true;
};

const postCsrfMiddleware = async function (ctx: Context, key: string): Promise<boolean>{
    const body = await ctx.request.body({ type: "json" }).value;
    
    const cookies_token = await ctx.cookies.get("token");
    var success = false;

    if (!body["csrf"] || !cookies_token || !computeVerifyHmacTokenPair(key, body["csrf"], cookies_token)){
        return success;
    }

    success = true;
    return success;
}

export default class csrfMiddleware extends Session {
    private key: string;

    constructor(key: string, store: any) {
      super(store);
      this.key = key;
    }

    csrf_protections(): Middleware {
        const csrf_func = async (ctx: Context, next: () => Promise<void>): Promise<void> => {
            if (ctx.request.method === "GET"){
                const get_success = await getCsrfMiddleware(ctx, this.key);
                if (!get_success) {
                    return ctx.response.status = Status.Forbidden;
                }
            } else if (ctx.request.method === "POST"){
                const post_success = await postCsrfMiddleware(ctx, this.key);
                if (!post_success){
                    return ctx.response.status = Status.Forbidden;
                }
            }
            await next();
        }
        return csrf_func as Middleware;
    }

}

