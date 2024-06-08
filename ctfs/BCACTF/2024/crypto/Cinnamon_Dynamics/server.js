import { createHash, timingSafeEqual } from 'crypto'
import { spawn } from 'child_process'
import { readFileSync } from 'fs'
import { join } from 'path'

import express from 'express'

const PORT = 3000

const secretKey = readFileSync('secret-key.txt', 'utf-8')

const app = express()

app.set('view engine', 'ejs')

app.use(express.urlencoded({ extended: true }))

app.get('/', (_req, res) => {
    res.render('index')
})

const safeCompare = (a, b) => {
    a = Buffer.from(a, 'utf-8')
    b = Buffer.from(b, 'utf-8')

    return a.length === b.length && timingSafeEqual(a, b)
}

app.post('/execute', (req, res) => {
    const { token, script } = req.body

    if (typeof token !== 'string' || typeof script !== 'string') {
        return res.render('execute', {
            error: 'Token and script must be provided and must be strings.'
        })
    }

    if (!script.trim().length) {
        return res.render('execute', {
            error: 'Please provide a script to execute.'
        })
    }

    const hash = createHash('sha256')
        .update(secretKey)
        .update(Buffer.from(script.replaceAll('\r\n', '\n'), 'binary'))

    if (!safeCompare(hash.digest('hex'), token)) {
        return res.render('execute', {
            error: 'Script token is invalid! ' +
                'Contact a Cinnamon Dynamics employee to get your script ' +
                'approved and receive a valid token for it.'
        })
    }

    const child = spawn('deno', ['run', '--allow-read=.', '-'], {
        cwd: join(process.cwd(), 'files'),
        env: { ...process.env, NO_COLOR: 1 }
    })

    let stdout = ''
    let stderr = ''

    child.stdout.on('data', data => stdout += data.toString('utf-8'))
    child.stderr.on('data', data => stderr += data.toString('utf-8'))

    child.stdin.write(req.body.script)
    child.stdin.end()

    let timedOut = false

    child.on('exit', exitCode => {
        res.render('execute', {
            error: timedOut ? 'Process timed out.' : null,
            stdout: stdout.trim(),
            stderr: stderr.trim(),
            exitCode
        })
    })

    setTimeout(() => {
        if (!child.killed) {
            timedOut = true
            child.kill('SIGKILL')
        }
    }, 1_000)
})

app.listen(PORT, () => console.log(`Server listening on port ${PORT}`))
