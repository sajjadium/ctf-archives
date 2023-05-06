import { crypto } from "https://deno.land/std@0.165.0/crypto/mod.ts";
import { getCookies } from "https://deno.land/std@0.165.0/http/cookie.ts";

const cookieName = 'enterprise-auth-token'

const secretKey = Deno.env.get('SECRET_KEY')

if (!secretKey) {
    throw new Error("SECRET_KEY missing")
}

const encoder = new TextEncoder('UTF-8')
const algorithm = { name: "HMAC", hash: "SHA-256" };

const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(secretKey),
    algorithm,
    false,
    ["sign", "verify"]
);

export async function sign(msg: string) {
    const raw = await crypto.subtle.sign(algorithm.name, key, encoder.encode(msg))

    return [...new Uint8Array(raw)].map(b => b.toString(16)).join('')
}

export async function verify(msg: string, sig: string) {
    const good = (await sign(msg)).split('')
    const check = sig.split('')

    if (good.length !== check.length) {
        return false
    }

    let passed = true;

    for (let i = 0; i < good.length; i++) {
        if (good[i] !== check[i]) {
            passed = false
        }
    }

    return passed
}

export async function setToken(user: string) {
    return {
        'content-type': 'text/html',
        'set-cookie': `${cookieName}=${user}:${await sign(user)}; domain=ctf.localhost`
    }
}

export async function getUser(req: Request) {
    const cookies = getCookies(req.headers)
    const token = cookies[cookieName]

    if (!token) {
        return null
    }

    const [user, sig] = token.split(':')

    if (user && sig && (await verify(user, sig)) === true) {
        return user
    }

    return null
}
