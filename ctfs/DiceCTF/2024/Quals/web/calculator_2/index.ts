import {
    default as express,
    Request,
    Response,
} from 'express'

import { run } from './jail'

const sanitize = (code: string): string => {
    return code
        .replaceAll(/</g, '&lt;')
        .replaceAll(/>/g, '&gt;')
        .replaceAll(/"/g, '&quot;')
}

const app = express()

const runQuery = async (query: string): Promise<string> => {
    if (query.length > 75) {
        return 'equation is too long'
    }

    try {
        const result = await run(query, 1000, 'number')

        if (result.success === false) {
            const errors: string[] = result.errors
            return sanitize(errors.join('\n'))
        } else {
            const value: number = result.value
            return `result: ${value.toString()}`
        }
    } catch (error) {
        return 'unknown error'
    }
}

app.get('/', async (req: Request, res: Response) => {
    const query = req.query.q ? req.query.q.toString() : ''
    const message = query ? await runQuery(req.query.q as string) : ''

    res.send(`
        <html>
            <body>
                <div>
                    <h1>Calculator</h1>
                    <form action="/" method="GET">
                        <input type="text" name="q" value="${sanitize(query)}">
                        <input type="submit">
                    </form>
                    <p>${message}</p>
                </div>
            </body>
        </html>
        <style>
            html, body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: grid;
                place-items: center;
            }
            p {
                max-width: 40ch;
            }
            div {
                min-width: 40ch;
                min-height: 20ch;
                border: 1px solid #aaa;
                border-radius: 5px;
                padding: 4rem;
            }
            input[type="text"] {
                width: 100%;
                padding: 0.5rem;
                margin-bottom: 1rem;
            }
        </style>
    `)
})

app.listen(3000)
