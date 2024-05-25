import crypto from 'crypto'
import fs from 'fs'
import http from 'http'
import path from 'path'

import { TRPCError, initTRPC } from '@trpc/server'
import { nodeHTTPRequestHandler } from '@trpc/server/adapters/node-http'
import { z } from 'zod'

const trpc = initTRPC.context<{
    user?: string,
    password?: string,
}>().create({})

const users = new Map<string, string>()
const pictures = new Map<string, { data: string, type: string }>()
const tickles = new Map<string, number>()

const publicProcedure = trpc.procedure.use(({ next }) => {
    return next({ ctx: {} })
})

const authedProcedure = trpc.procedure.use(({ next, ctx }) => {
    if (!ctx.user || !ctx.password) {
        throw new TRPCError({ code: 'UNAUTHORIZED' })
    }
    if (users.get(ctx.user) !== ctx.password) {
        throw new TRPCError({ code: 'UNAUTHORIZED' })
    }
    return next({ ctx: { user: ctx.user, password: ctx.password } })
})

const router = trpc.router({
    user: authedProcedure.query(({ ctx }) => {
        return { success: true as const, user: ctx.user }
    }),

    doRegister: publicProcedure
        .input(z.object({
            username: z.string(),
            password: z.string(),
        }))
        .mutation(({ input: { username, password } }) => {
            if (users.has(username)) {
                return {
                    success: false as const,
                    message: 'User already exists.',
                }
            }
            users.set(username, password)
            return { success: true as const }
        }),

    doLogin: publicProcedure
        .input(z.object({
            username: z.string(),
            password: z.string(),
        }))
        .mutation(({ input: { username, password } }) => {
            if (users.get(username) === password) {
                return { success: true as const }
            }
            return { success: false as const, message: 'Invalid credentials.' }
        }),

    doTickle: authedProcedure
        .input(z.object({ username: z.string() }))
        .mutation(({ input: { username }, ctx }) => {
            if (!users.has(username)) {
                return {
                    success: false as const,
                    message: 'User does not exist.',
                }
            }

            if (username === ctx.user) {
                return {
                    success: false as const,
                    message: 'Nice try.',
                }
            }

            const count = tickles.get(username) ?? 0
            tickles.set(username, count + 1)

            return { success: true as const }
        }),

    getTickles: publicProcedure
        .input(z.object({ username: z.string() }))
        .query(({ input: { username } }) => {
            if (!users.has(username)) {
                return {
                    success: false as const,
                    message: 'User does not exist.',
                }
            }
            return {
                success: true as const,
                count: tickles.get(username) ?? 0,
            }
        }),

    getFlag: authedProcedure.query(({ ctx }) => {
        if (tickles.get(ctx.user) !== Infinity) {
            return { success: false as const, message: 'Not enough tickles.' }
        }
        return { success: true as const, flag: process.env.FLAG }
    }),

    setPicture: authedProcedure
        .input(z.object({ url: z.string() }))
        .mutation(async ({ input: { url }, ctx }) => {
            let response
            try {
                response = await fetch(url)
            } catch {
                return {
                    success: false as const,
                    message: 'Failed to fetch image.',
                }
            }

            if (!response.ok) {
                return {
                    success: false as const,
                    message: 'Failed to fetch image.',
                }
            }

            const reader = response.body?.getReader()
            if (reader === undefined) {
                return {
                    success: false as const,
                    message: 'No image data.',
                }
            }

            let size = 0
            const data = []
            while (true) {
                const { done, value } = await reader.read()
                if (done) break
                size += value.byteLength
                if (size > 1e6) {
                    return {
                        success: false as const,
                        message: 'Image too large.',
                    }
                }
                data.push(value)
            }

            const buffer = new Blob(data)
            const array = await buffer.arrayBuffer()
            const base64 = Buffer.from(array).toString('base64')
            pictures.set(ctx.user, {
                data: base64,
                type: response.headers.get('content-type') ?? 'image/png',
            })

            return { success: true as const }
        }),
})

const mime = new Map([
    ['css', 'text/css'],
    ['html', 'text/html'],
    ['js', 'application/javascript'],
])

const send = (res: http.ServerResponse, file: string) => {
    const ext = path.extname(file).slice(1)
    res.setHeader('content-type', mime.get(ext) ?? 'text/plain')

    const stream = fs
        .createReadStream(file)
        .on('error', () => {
            res.writeHead(404)
            res.end()
        })
        .pipe(res)

    stream.on('close', () => {
        res.end()
    })
}

const server = http.createServer(async (req, res) => {
    res.setHeader('content-security-policy', 'script-src \'self\'')

    const url = req.url ?? ''
    let route = url
    if (route.includes('?')) {
        route = route.slice(0, route.indexOf('?'))
    }
    route = path.normalize(`/${route ?? ''}`)

    const end = () => {
        res.writeHead(404)
        res.end()
    }

    if (route === '/admin') {
        if (process.env.ADMIN === undefined) return end()

        const body: Buffer[] = []
        req.on('data', (chunk) => body.push(chunk))
        await new Promise((resolve) => req.on('end', resolve))

        const data = Buffer.concat(body).toString()
        if (data !== process.env.ADMIN) return end()

        const username = crypto.randomBytes(16).toString('hex')
        const password = crypto.randomBytes(16).toString('hex')

        users.set(username, password)
        tickles.set(username, Infinity)

        res.setHeader('content-type', 'application/json')
        return res.end(JSON.stringify({ username, password }))
    } else if (route === '/picture') {
        if (!url.includes('?')) return end()

        const query = new URLSearchParams(url.slice(url.indexOf('?')))
        const username = query.get('username')

        if (username === null) return end()

        const picture = pictures.get(username)
        if (picture === undefined) return end()

        const { data, type } = picture
        res.end(`data:${type};base64,${data}`)
    } else if (route.startsWith('/api/')) {
        await nodeHTTPRequestHandler({
            router,
            req,
            res,
            path: route.slice('/api/'.length),
            createContext: ({ req }) => {
                const header = req.headers.login
                const clean = Array.isArray(header) ? header[0] : header ?? ''
                const [user, password] = clean.split(':') ?? []
                return { user, password }
            },
        })
    } else {
        if (route === '/') route = '/index.html'
        else if (!route.includes('.')) route += '.html'
        send(res, path.join(import.meta.dirname, 'public', route))
    }
})

server.listen(3000, () => {
    console.log('running on :3000')
})

export type Router = typeof router
