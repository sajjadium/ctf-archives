import { serve } from "https://deno.land/std@0.165.0/http/server.ts";
import {redirect, template, templateResponse} from "./template.ts";

import {getUser, setToken} from "./auth.ts";

interface RouteEntry {
    method: string[],
    handler: (Request) => Response,
    pattern: URLPattern
}

interface User {
    password: string
}

const users: Map<string, User> = new Map()

async function index(req: Request) {
    if (!(await getUser(req)))  {
        return redirect('/login')
    }

    return templateResponse("Hello world")
}

async function register(req: Request) {
    if (await getUser(req))  {
        return redirect('/')
    }

    if (req.method === 'GET') {
        return templateResponse(`
            <h3>Register for our awesome tools</h3>

            <form method="POST" action="/register">
                <input name="username" type="text" placeholder="Username"><br>
                <input name="password" type="password" placeholder="Password"><br>
                <input type="submit" value="Register">
            </form>
        `)
    }

    const body = await req.formData()

    if (!body.has('username') || !body.has('password')) {
        return templateResponse("Missing fields")
    }

    const name = body.get('username').toLowerCase().trim()

    if (name.length > 20 || name.match('/admin/ig') || users.has(name)) {
        return templateResponse("Invalid username")
    }

    users.set(name, {
        password: body.get('password')
    })

    console.log(`[registration] user: ${name} password: ${body.get('password')}`)

    return templateResponse(`<h3>Registration completed<h3> Continue to <a href="/login">login</a>`)
}

async function login(req: Request) {
    if (await getUser(req))  {
        return redirect('/')
    }

    if (req.method === 'GET') {
        return templateResponse(`
            <h3>Please login</h3>

            <form method="POST" action="/login">
                <input name="username" type="text" placeholder="Username"><br>
                <input name="password" type="password" placeholder="Password"><br>
                <input type="submit" value="Login">
            </form><br>
            
            <a href="/register">Register</a>
        `)
    }

    const body = await req.formData()

    if (!body.has('username') || !body.has('password')) {
        return templateResponse("Missing fields")
    }

    const name = body.get('username').toLowerCase().trim()
    const user = users.get(name)

    console.log(`[login] user: ${name} password: ${body.get('password')}`)

    if (!user || body.get('password') !== user.password) {
        return templateResponse("Login Failed")
    }

    const resp = template("Login success")

    return new Response(resp, { headers: await setToken(name) })
}

async function auth(req: Request) {
    const user = await getUser(req)

    console.log(`[auth] user: ${user} uri: ${req.headers.get('X-Forwarded-Uri')}`)

    if (!user) {
        return redirect('http://auth.ctf.localhost:8844')
    }

    return new Response(null, {
        headers: {
            "remote-user": user
        }
    })
}

function mkRoute(pattern, handler, methods = ['GET']): RouteEntry {
    return { methods, url: new URLPattern({ pathname: pattern}), handler }
}

const routes: RouteEntry[] = [
    mkRoute('/', index),
    mkRoute('/register', register, ['GET', 'POST']),
    mkRoute('/login', login, ['GET', 'POST']),
    mkRoute('/auth', auth)
]

function router(req: Request): Response {
    const route = routes.find(route => route.methods.includes(req.method) && route.url.exec(req.url))

    if (route) {
        return route.handler(req)
    }

    return new Response("Not found", {
        status: 404,
    });
}

console.log("Listening on http://localhost:8000");
serve(router);
