import express from 'express';
import fetch from 'node-fetch';

if (!process.env.FLAG) {
    throw new Error('FLAG must be set');
}

const server = express();

server.use(express.static('public'));

server.post("/ping", express.json(), async function (req, res) {
    const errors = [];
    const noneHexRegex = /[^0-9a-f]/g;
    const fqdns = Array.isArray(req.body.fqdn) ? req.body.fqdn : [req.body.fqdn];

    if (fqdns.length >= 5) {
        return res.status(400).json({ error: 'Too many FQDNs' });
    }

    for (let fqdn of fqdns) {
        if (typeof fqdn !== "string") {
            errors.push(`${fqdn} must be a string`);
            continue;
        }

        if (noneHexRegex.test(fqdn)) {
            errors.push(`${fqdn} should only contain hexadecimal characters`);
            continue;
        }

        let buf = Buffer.from(fqdn, "hex");

        if (buf.length !== 16) {
            errors.push(`${fqdn} must be 16 bytes long`);
            continue;
        }

        const url = `http://${fqdn}.ping-proxy/ping`;

        try {
            await fetch(url, {
                headers: {
                    'X-FLAG': process.env.FLAG
                }
            });
        } catch (err) {
            errors.push(err.message);
        }
    }

    if (errors.length > 0) {
        res.status(500);
    }

    res.json({ errors });
});

server.listen(1337, function (err) {
    if (err) {
        throw err;
    }
    console.log('Server is up and running on http://localhost:1337');
});
