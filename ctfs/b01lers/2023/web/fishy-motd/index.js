import fastify from 'fastify';
import fastifyFormbody from '@fastify/formbody';
import fastifyStatic from '@fastify/static';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import puppeteer from 'puppeteer';
import { nanoid } from 'nanoid';

let messages = {}

const server = fastify();

server.register(fastifyFormbody);
server.register(fastifyStatic, {
    root: path.join(path.dirname(fileURLToPath(import.meta.url)), 'public'),
    prefix: '/public/'
});

const flag = process.env.FLAG || 'flag{fake_flag}';
const port = 5000;
const user = process.env.ADMIN_USER || 'admin';
const pass = process.env.ADMIN_PASS || 'pass';

server.get('/', (req, res) => {
    res.sendFile('index.html')
});

server.get('/style.css', (req, res) => {
    res.sendFile('style.css')
});

server.get('/login', (req, res) => {
    const id = req.query.motd;
    if (!id) {
        fs.readFile('./login.html', 'utf8', (err, data) => {
            if (err) {
                console.log(err);
                res.status(500).send('Internal server error, please open a ticket');
            }
            else {
                res.type('text/html').send(data.toString().replace('{{motd}}', 'Welcome to the server!'));
            }
        });
    }
    else {
        if (id in messages) {
            fs.readFile('./login.html', 'utf8', (err, data) => {
                if (err) {
                    console.log(err);
                    res.status(500).send('Internal server error, please open a ticket');
                }
                else {
                    res.type('text/html').send(data.toString().replace('{{motd}}', messages[id]));
                }
            });
        } else {
            res.send('MOTD not found');
        }
    }
});

server.post('/login', (req, res) => {
    const username = req.body.username;
    const password = req.body.password;

    if (username === user && password === pass) {
        res.send(flag);
    }
    else {
        res.send('Incorrect username or password');
    }
});

server.get('/start', async (req, res) => {
    const id = req.query.motd;
    if (id && id in messages) {
        try {
            const result = await adminBot(id);
            if (result.error) {
                res.send(result.error)
            } else {
                res.send('Hope everyone liked your message!')
            }
        } catch (err) {
            console.log(err);
            res.send('Something went wrong, please open a ticket');
        }
    } else {
        res.send('MOTD not found');
    }
});

server.post('/motd', (req, res) => {
    const motd = req.body.motd;
    const id = nanoid();
    messages[id] = motd;
    fs.readFile('./motd.html', 'utf8', (err, data) => {
        if (err) {
            console.log(err);
            res.status(500).send('Internal server error, please open a ticket');
        }
        else {
            res.type('text/html').send(data.toString().replaceAll('{{id}}', id));
        }
    });
})

server.get('/motd', (req, res) => {
    res.send('Please use the form to submit a message of the day.');
});

const adminBot = async (id) => {
    const browser = await puppeteer.launch({
        headless: true, // Uncomment below if the sandbox is causing issues
        // args: ['--no-sandbox', '--disable-setuid-sandbox', '--single-process']
    })
    const page = await browser.newPage();
    await page.setViewport({ width: 800, height: 600 });
    const url = `http://localhost:${port}/login?motd=${id}`;
    await page.goto(url);
    await page.mouse.click(10, 10);
    await new Promise(r => setTimeout(r, 1000));
    try {
        if (url !== await page.evaluate(() => window.location.href)) {
            return { error: "Hey! Something's fishy here!" };
        }
    } catch (err) {
        return { error: "Hey! Something's fishy here!" };
    }
    await new Promise(r => setTimeout(r, 5000));
    await page.mouse.click(420, 280);
    await page.keyboard.type(user);
    await page.mouse.click(420, 320);
    await page.keyboard.type(pass);
    await page.mouse.click(420, 360);
    await new Promise(r => setTimeout(r, 1000));
    await browser.close();
    messages[id] = undefined;
    return { error: null };
}

server.listen({ port, host: '0.0.0.0' }, (err, address) => {
    if (err) {
        console.error(err);
        process.exit(1);
    }
    console.log(`Server listening at ${address}`);
});