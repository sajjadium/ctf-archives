const express = require('express')

const app = express()

const cookies = new Map()

app.use((req, res, next) => {
    const cookies = req.headers.cookie
    const user = cookies?.split('=')?.[1]

    if (user) { req.user = user }
    else {
        const id = Math.random().toString(36).slice(2)
        res.setHeader('set-cookie', `user=${id}`)
        req.user = id
    }

    next()
})

app.get('/', (req, res) => {
    const count = cookies.get(req.user) ?? 0
    res.type('html').send(`
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@exampledev/new.css@1/new.min.css">
        <link rel="stylesheet" href="https://fonts.xz.style/serve/inter.css">
        <div>You have <span>${count}</span> cookies</div>
        <button id="basic">Basic cookie recipe (makes one)</button>
        <br>
        <button id="advanced">Advanced cookie recipe (makes a dozen)</button>
        <br>
        <button disabled>Super cookie recipe (makes a million)</button>
        <br>
        <button id="deliver">Deliver cookies</button>
        <script src="/script.js"></script>
    `)
})

app.get('/script.js', (_req, res) => {
    res.type('js').send(`
        const basic = document.querySelector('#basic')
        const advanced = document.querySelector('#advanced')
        const deliver = document.querySelector('#deliver')

        const showCookies = (number) => {
            const span = document.querySelector('span')
            span.textContent = number
        }

        basic.addEventListener('click', async () => {
            const res = await fetch('/bake?number=1', { method: 'POST' })
            const number = await res.text()
            showCookies(+number)
        })

        advanced.addEventListener('click', async () => {
            const res = await fetch('/bake?number=12', { method: 'POST' })
            const number = await res.text()
            showCookies(+number)
        })


        deliver.addEventListener('click', async () => {
            const res = await fetch('/deliver', { method: 'POST' })
            const text = await res.text()
            alert(text)
        })
    `)
})

app.post('/bake', (req, res) => {
    const number = req.query.number
    if (!number) {
        res.end('missing number')
    } else if (number.length <= 2) {
        cookies.set(req.user, (cookies.get(req.user) ?? 0) + Number(number))
        res.end(cookies.get(req.user).toString())
    } else {
        res.end('that is too many cookies')
    }
})

app.post('/deliver', (req, res) => {
    const current = cookies.get(req.user) ?? 0
    const target = 1_000_000_000
    if (current < target) {
        res.end(`not enough (need ${target - current}) more`)
    } else {
        res.end(process.env.FLAG)
    }
})

app.listen(3000)
