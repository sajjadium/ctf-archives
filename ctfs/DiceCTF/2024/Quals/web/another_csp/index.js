import { createServer } from 'http';
import { readFileSync } from 'fs';
import { spawn } from 'child_process'
import { randomInt } from 'crypto';

const sleep = timeout => new Promise(resolve => setTimeout(resolve, timeout));
const wait = child => new Promise(resolve => child.on('exit', resolve));
const index = readFileSync('index.html', 'utf-8');

let token = randomInt(2 ** 24).toString(16).padStart(6, '0');
let browserOpen = false;

const visit = async code => {
	browserOpen = true;
	const proc = spawn('node', ['visit.js', token, code], { detached: true });

	await Promise.race([
		wait(proc),
		sleep(10000)
	]);

	if (proc.exitCode === null) {
		process.kill(-proc.pid);
	}
	browserOpen = false;
}

createServer(async (req, res) => {
	const url = new URL(req.url, 'http://localhost/');
	if (url.pathname === '/') {
		return res.end(index);
	} else if (url.pathname === '/bot') {
		if (browserOpen) return res.end('already open!');
		const code = url.searchParams.get('code');
		if (!code || code.length > 1000) return res.end('no');
		visit(code);
		return res.end('visiting');
	} else if (url.pathname === '/flag') {
		if (url.searchParams.get('token') !== token) {
			res.end('wrong');
			await sleep(1000);
			process.exit(0);
		}
		return res.end(process.env.FLAG ?? 'dice{flag}');
	}
	return res.end();
}).listen(8080);