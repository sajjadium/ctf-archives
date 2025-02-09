import Fastify from 'fastify';
const fastify = Fastify();
import HTMLParser from 'node-html-parser';
import fs from 'fs';
const box = fs.readFileSync('./index.html', 'utf-8');

fastify.get('/', (req, res) => {
    const note = req.query.note;
    const trustedDomains = [];
    if (note) {
        const parsed = HTMLParser.parse(note);
        const elements = parsed.getElementsByTagName('*');
        for (let el of elements) {
            const src = el.getAttribute('src');
            if (src) {
                trustedDomains.push(src);
            }
        }
    }

    const csp = [
        "default-src 'none'",
        "style-src 'unsafe-inline'",
        "script-src 'unsafe-inline'"
    ];

    if (trustedDomains.length) {
        csp.push(`img-src ${trustedDomains.join(' ')}`);
    }

    res.header('Content-Security-Policy', csp.join('; '));
    res.type('text/html');
    return res.send(box);
});


