import http from 'http'
import { readFileSync } from 'fs';
import { VM } from 'vm2'

const flag = readFileSync('/flag.txt');

http.createServer((req, res) => {
    const url = new URL('http://127.0.0.1:8080/' + req.url);
    res.writeHead(200, {'Content-Type': 'text/plain'});
    try {
        res.write(Buffer.from(new String(new VM({
            timeout: 1000,
            allowAsync: false,
            sandbox: {}
        }).run(url.searchParams.get('exploit') ?? ""))));
    } catch(e) {}
    res.end()
}).listen(8080, '0.0.0.0');