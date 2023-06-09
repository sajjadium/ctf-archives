import {get, ServerResponse} from 'http';
import polka from 'polka';
import fs from 'fs/promises';
import {dirname} from 'path';
import {fileURLToPath} from 'url';
import {randomBytes, createHmac, timingSafeEqual} from 'crypto';
import {PrismaClient} from "@prisma/client";
import bodyParser from "body-parser";
import puppeteer from "puppeteer";

const __dirname = dirname(fileURLToPath(import.meta.url));
const pages = new Map<string, string>()

await Promise.all(['index', 'checkout', 'confirmation'].map(async p => {
    pages.set(p, (await fs.readFile(`${__dirname}/static/${p}.html`)).toString())
}))

const secretKey = randomBytes(128)

const sign = (value: string) => {
    return createHmac('sha256', secretKey)
        .update(value)
        .digest('base64url')
}

const prisma = new PrismaClient()
const app = polka({
    onError(err: Error, req: polka.Request, res: ServerResponse, next: polka.Next) {
        console.error(err)

        res.end('Unknown error')
    },

    onNoMatch(req: polka.Request, res: ServerResponse) {
        res.end('Page not found')
    }
});

app.use(bodyParser.urlencoded({extended: false}))

app.get('/', async (req, res) => {
    const products = await prisma.item.findMany({
        select: {id: true, title: true, price: true, description: true}
    })

    return res.end(
        pages.get('index')!.replace(':data', JSON.stringify(products))
    )
})

app.get('/checkout/:product', async (req, res) => {
    const item = await prisma.item.findFirstOrThrow({
        where: {id: parseInt(req.params.product)}
    })

    return res.end(
        pages.get('checkout')!.replace(':title', item.title)
    )
})

app.get('/_internal/pdf', async (req, res) => {
    const id = req.query.id || '0'
    const title = req.query.title || ''
    const email = req.query.email || ''
    const content = req.query.content || ''

    if (typeof id !== 'string' || typeof title !== 'string' || typeof email !== 'string' || typeof content !== 'string') {
        return res.end(':(')
    }

    const body = pages.get('confirmation')!
        .replace(':title', title)
        .replace(':email', email)
        .replace(':content', content)

    res.end(body)
})

let rendererInUse = false

app.post('/checkout/:product', async (req, res) => {
    if (!req.body.email) {
        res.end('Missing email')
    }

    const item = await prisma.item.findFirstOrThrow({
        where: {id: parseInt(req.params.product)}
    })

    if (item.price !== 0) {
        return res.end("Our payment processor went bankrupt and as a result we can't accept payments right now. Please check back later or have a look at our free offerings")
    }

    while (rendererInUse) {
        await new Promise(resolve => setTimeout(resolve, 100))
    }

    rendererInUse = true
    let browser = null

    try {
        browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--js-flags="--jitless"']
        })
        const page = await browser.newPage()


        const u = new URL('http://127.0.0.1:8000/_internal/pdf')
        u.search = new URLSearchParams({
            id: item.id.toString(),
            email: req.body.email as string,
            title: item.title as string,
            content: item.download as string
        }).toString()

        await page.goto(u.toString(), {waitUntil: 'networkidle0', timeout: 30000})

        res.end(await page.pdf({format: 'A4', timeout: 1000}))
    } catch (e) {
        res.end(':(')
    } finally {
        if (browser) await browser.close()
        rendererInUse = false
    }
})

app.listen(8000);
console.log("Running");
