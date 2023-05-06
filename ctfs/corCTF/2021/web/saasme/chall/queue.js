const spawn = require('child_process').spawn;
let queue = [], running = false, proc;

function run(url) {
	return new Promise((resolve, reject) => {
		console.log('[BROWSER] Visiting', url);

		let start = Date.now();
		let closed = false;

		proc = spawn('node', ['browser.js', url], {
			stdio: 'inherit',
			detached: true
		});

		let timeout = setTimeout(() => {
			if (!closed) process.kill(-proc.pid)
		}, 45 * 1000);

		proc.on('exit', code => {
			closed = true;
			clearTimeout(timeout);

			console.log(`[BROWSER] Session closed with code ${code}, took ${Math.round((Date.now() - start) / 1000)} s`);
			
			resolve();
		});

		proc.on('error', (err) => {
			console.log('[BROWSER] Failed to spawn process');
			console.error(err);
		});
	})
}

function next() {
	if (queue.length === 0) return;

	(async () => {
		running = true;
		await run(queue.shift());
		running = false;

		next();
	})();
}


function add(url) {
	queue.push(url);

	if (!running) {
		next();
	}
}

function kill() {
	if (running) {
		process.kill(-proc.pid);
	}
}

module.exports = {
	add,
	kill
}