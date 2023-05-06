import cluster from "cluster";

if (cluster.isPrimary) {
	// eslint-disable-next-line no-console
	console.log(`Primary process is running with PID: ${process.pid}`);

	import("./Primary.js").then(({ Primary }) => {
		const primary = new Primary();
		primary.start();
	});
} else {
	const workerId = cluster.worker!.id;
	// eslint-disable-next-line no-console
	console.log(`Worker process ${workerId} is running with PID: ${process.pid}`);

	import("./Worker.js").then(({ Worker }) => {
		const worker = new Worker(workerId);
		worker.start();
	});
}
