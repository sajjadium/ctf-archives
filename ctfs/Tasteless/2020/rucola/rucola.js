const vm = require('vm');
const http = require('http');
const https = require('https');

const HOST = "";
const PORT = 11001;

class ScoringAlgorithm {
	static ALLOWED_URL_PREFIX = "http://127.0.0.1:1338/";
	static ALLOWED_MODULE_PATTERN = "^(console)|(https?)|(net)$"

	constructor(url) {
		this.__script = undefined;
		this.__url = url;
	}

	async getScript() {
		if (this.__script) {
			return this.__script;
		}
		this.__script = ScoringAlgorithm.fetchScript(this.__url);
		return this.__script;
	}

	static isValidUrl(url) {
		return url.startsWith(ScoringAlgorithm.ALLOWED_URL_PREFIX);
	}

	static async fetchScript(url) {
		if (!ScoringAlgorithm.isValidUrl(url)) {
			throw new Error('Scoring Algorithms can only be downloaded from the Official Store!');
		}

		return new Promise((resolve, reject) => {
			const client = url.startsWith("https") ? https : http;
			client.get(url, (res) => {
				if (res.statusCode != 200) {
					reject(new Error(`HTTP Error: ${res.statusCode}`));
				}

				let data = '';
				res.on('data', (chunk) => data += chunk );
				res.on('end', () => resolve(data));
			}).on("error", (err) => reject(err));
		});
	}

	async run(ratings) {
		const pattern = new RegExp(ScoringAlgorithm.ALLOWED_MODULE_PATTERN);
		const safe_require = function (mod) {
			if (!pattern.test(mod)) {
				throw new Error("Permission Denied!");
			}

			return require(mod);
		}

		return this.getScript().then(
			(script) => vm.runInNewContext(script, {
				ratings: ratings,
				safe_require: safe_require,
				log: console.log
			}),
			(e) => e
		);
	}
}


class CTFs {
	constructor() {
		this.__storage = {};
	}

	get list() {
		let ret = [];

		for (let ctf of Object.values(this.__storage)) {
			ret.push(ctf.name);
		}

		return ret;
	}

	getCTF(name) {
		if (this.hasCTF(name)) {
			return this.__storage[CTFs.getCTFId(name)];
		} else {
			throw new Error("CTF does not exist");
		}
	}

	static getCTFId(name) {
		return `ctf_${name}`;
	}

	hasCTF(name) {
		return this.__storage.hasOwnProperty(CTFs.getCTFId(name))
	}

	create(name, ...args) {
		if (this.hasCTF(name)) {
			throw new Error("Challenge already exists!");
		}

		this.__storage[CTFs.getCTFId(name)] = new CTF(name, ...args);
	}
}


class CTF {
	constructor(name, scoringAlgorithm) {
		this.name = name,
		this.scoringAlgorithm = scoringAlgorithm;
		this.__challenges = {};
	}

	get challenges() {
		return this.__challenges;
	}

	get public_data() {
		return {
			name: this.name,
			challenges: Object.values(this.challenges).map((chall) => { return { name: chall.name, points: chall.points }}),
		};
	}

	static getChallengeId(name) {
		return `challenge_${name}`;
	}

	getChallenge(name) {
		if (!this.hasChallenge(name)) {
			throw new Error("Challenge does not exist");
		}

		return this.__challenges[CTF.getChallengeId(name)];
	}

	hasChallenge(name) {
		return this.__challenges.hasOwnProperty(CTF.getChallengeId(name));
	}

	addChallenge(name, points, checker) {
		if (this.hasChallenge(name)) {
			throw new Error("Challenge already exists!");
		}

		let challenge = new Challenge(name, points, checker, this);

		challenge.ctf = this;
		this.__challenges[CTF.getChallengeId(name)] = challenge;
	}

	get ratings() {
		return Object.values(this.__challenges).map((challenge) => {
			return {
				name: challenge.name,
				points: challenge.points,
				solves: challenge.solves,
			};
		});
	}

	update_ratings () {
		return this.scoringAlgorithm.run(this.ratings)
			.then(
				(new_ratings) => {
					for (let challenge of new_ratings) {
						if (!this.hasChallenge(challenge.name) || !(challenge.points instanceof Number))
							throw new Error("Scoring algorithm provided invalid output");
					}

					for (let challenge of new_ratings) {
						this.getChallenge(challenge.name).points = challenge.points;
					}
				},
				() => {}
			);
	}
}


class Challenge {
	constructor(name, points, checker, ctf) {
		this.name = name;
		this.points = points;
		this.ctf = ctf;

		this.__checker = checker || "input === 'flag{defualt}' ? Promise.resolve() : Promise.reject()";
		this.__solves = new Set();
	}

	solve(user, flag) {
		return vm.runInNewContext(this.__checker, {
				input: flag,
				log: console.log,
				Promise: Promise,
				RegExp: RegExp
			})
			.then(() => this.__solves.add(user))
			.then(() => this.ctf.update_ratings());
	}

	get solves() {
		return this.__solves;
	}

	get checker() {
		throw new Error("Can't get the checker, it might contain the flag!");
	}

	set checker(value) {
		if (value instanceof String) {
			this.__checker = value;
		} else {
			throw new Error("invalid checker function");
		}
	}

	get public_data() {
		return {
			name: this.name,
			points: this.points,
			solves: Array.from(this.solves)
		}
	}
}


class Route {
	constructor (req, res, path, ancestors) {
		this.req = req;
		this.res = res;
		this.ancestors = ancestors || [];

		try {
			this.path = path || decodeURI(req.url);
		} catch {
			return this.fail(400);
		}

		const match = this.pattern.exec(this.path);
		if (match === null) {
			throw new Error("unknown path");
		}

		for (const group of Object.keys(match.groups)) {
			this[group] = match.groups[group];
		}

		switch(this.suffix) {
			case undefined:
			case "":
			case "/":
				this.handle();
				return;
			default:
				this.recurse(this.suffix.substring(1));
				return;
		}
	}

	respond(body, options) {
		options = {
			status: 200,
			headers: {},
			...options
		};
		const status = options.status || 200;
		this.res.writeHead(status, options.headers);
		this.res.end(`${body}\n`);
	}

	respondJson(data, options) {
		options = options || {};
		options.headers = {
			...(options.headers || {}),
			'Content-Type': 'application/json'
		};
		try {
			return this.respond(JSON.stringify(data), options);
		} catch(e) {
			return this.fail(500);
		}
	}

	fail(statusCode, customText) {
		const statusText = {
			400: "Bad Request",
			403: "Forbidden",
			404: "Not Found",
			405: "Method Not Allowed",
			409: "Conflict",
			418: "I'm a Teapot",
			500: "Internal Server Error",
		};
		const body = customText || statusText[statusCode] || "Error";
		this.respond(body, { status: statusCode });
	}

	redirect(url) {
		return this.respond("", {
			status: 302,
			headers: {
				"Location": encodeURI(url)
			}
		});
	}

	handle() {
		const method = this.req.method.toUpperCase();
		const handler = this[method];
		if (handler === undefined) {
			return this.fail(405);
		}
		switch (method) {
			case "POST":
				if (this.req.headers['content-type'] !== 'application/json') {
					return this.fail(400, "application/json expected");
				}

				const self = this;
				let body = "";
				this.req.on('data', chunk => body += chunk.toString());
				this.req.on('end', () => {
					try {
						self.json = JSON.parse(body);
					} catch {
						return self.fail(400);
					}
					handler.call(self);
				});
				return;

			case "GET":
				return handler.call(this);

			default:
				return this.fail(405);
		}
	}

	__failRecursion() {
		this.fail(404);
	}

	recurse(path) {
		for (const SubRoute of this.subRoutes) {
			try {
				const ancestors = [this].concat(this.ancestors);
				const subRoute = new SubRoute(this.req, this.res, path, ancestors);
				return subRoute;
			} catch {
			}
		}
		this.__failRecursion();
	}

	get subRoutes() {
		return [];
	}
}

class Index extends Route {
	get pattern() {
		return new RegExp("^(?<suffix>/.*)$");
	}

	GET() {
		this.respond("Welcome to the CTF");
	}

	get subRoutes() {
		return [ CTFsView ];
	}
}

class CTFsView extends Route {
	get pattern() {
		return new RegExp("^ctf(?<suffix>/.*)?$");
	}

	GET() {
		return this.respondJson(ctfs.list);
	}

	POST() {
		const ctf = this.json;

		if (!(typeof(ctf.name) === "string")) {
			return this.fail(400, "CTF name required");
		}

		if  (!typeof(ctf.scoring_algorithm) === "string") {
			return this.fail(400, "Scoring algorithm required");
		}

		if (ctfs.hasCTF(ctf.name)) {
			return this.fail(409, "CTF already exists");
		}

		const scoring_algorithm = new ScoringAlgorithm(ctf.scoring_algorithm);

		try {
			ctfs.create(ctf.name, scoring_algorithm);
		} catch(e) {
			return this.fail(500, e.message);
		}

		this.redirect(`/ctf/${ctf.name}/`);
	}

	get subRoutes() {
		return [ CTFView ];
	}
}

class CTFView extends Route {
	get pattern() {
		return new RegExp("^(?<name>[\\w ]+)(?<suffix>/.*)?$");
	}

	get ctf() {
		return ctfs.getCTF(this.name);
	}

	GET() {
		try {
			this.respondJson(this.ctf.public_data);
		} catch {
			this.fail(404);
		}
	}

	get subRoutes() {
		return [ ChallengesView ];
	}
}

class ChallengesView extends Route {
	get pattern() {
		return new RegExp("^challenges?(?<suffix>/.*)?$");
	}

	get ctf() {
		return this.ancestors[0].ctf;
	}

	GET() {
		try {
			const challenges = this.ctf.challenges;
		} catch {
			return this.fail(404);
		}

		this.respondJson(
			Object.values(challenges).map(((chall) => chall.public_data))
		);
	}

	POST() {
		const challenge = this.json;

		if (!(typeof(challenge.name) == "string"
			&& typeof(challenge.points) == "number" && !Number.isNaN(Number(challenge.points))
			&& typeof(challenge.checker) == "string"))
		{
			return this.fail(400);
		}

		if (!/[\w]+/.test(challenge.name))
			this.fail(400);

		if (this.ctf.hasChallenge(challenge.name))
			this.fail(409);

		try {
			this.ctf.addChallenge(challenge.name, challenge.points, challenge.checker);
		} catch (e) {
			return this.fail(400)
		}
		return this.redirect(`/ctf/${this.ctf.name}/challenge/${challenge.name}`);
	}

	get subRoutes() {
		return [ ChallengeView ];
	}
}

class ChallengeView extends Route {
	get pattern() {
		return new RegExp("^(?<name>[\\w ]+)(?<suffix>/.*)?$");
	}

	get ctf() {
		return this.ancestors[1].ctf;
	}

	get challenge() {
		if (!this.ctf.hasChallenge(this.name)) {
			throw new Error("No such challenge");
		}

		return this.ctf.getChallenge(this.name);
	}

	GET() {
		try {
			this.respondJson(this.challenge.public_data);
		} catch {
			this.fail(404);
		}
	}

	get subRoutes() {
		return [ SolveView ];
	}
}

class SolveView extends Route {
	get pattern() {
		return new RegExp("^solve(?<suffix>/.*)?$");
	}

	get challenge() {
		return this.ancestors[0].challenge;
	}

	POST() {
		let challenge;
		try {
			challenge = this.challenge;
		} catch {
			return this.fail(404);
		}

		const attempt = this.json;

		if (!(attempt.hasOwnProperty('flag') && attempt.hasOwnProperty('user'))) {
			return this.fail(400);
		}

		challenge.solve(attempt.user, attempt.flag)
		.then(
			() => this.respondJson({valid: true}),
			(e) => {
				if (e instanceof Error) {
					return this.fail(500);
				}

				this.respondJson({valid: false}, { status: 418 });
			}
		);
	}
}


class API {
	constructor(host, port) {
		this.__server = http.createServer((req, res) => {
			new Index(req, res)
		});
		this.__server.listen(port, host, () => {
			console.log(`Server is running on http://${host}:${port}`);
		});
	}
}

const ctfs = new CTFs();
const api = new API(HOST, PORT);
