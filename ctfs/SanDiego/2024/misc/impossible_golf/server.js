const express = require("express");
const http = require("http");
const app = express();
const path = require("path");
const { WebSocketServer } = require("ws");
const {readFileSync} = require("fs");

const server = http.createServer(app);

const wss = new WebSocketServer({server: server});

const FLAG = readFileSync(path.join(__dirname, "flag.txt")).toString();

wss.on("connection", ws => {
	console.log("New connection!");
	let level = 0;
	let gameState = JSON.parse(JSON.stringify(levels[level]));
	let interval = setInterval(physicsLoop, 20);
	let goalTimer = 0;

	function physicsLoop() {
		applyVelocity(gameState.circle, gameState.rects);

		for (let obj of gameState.rects) {
			circleRectCollision(gameState.circle, obj);
		}
		if (circlesIntersecting(gameState.goal, gameState.circle)) {
			goalTimer++;
		} else {
			goalTimer = 0;
		}
		if (goalTimer > 50) {
			level++;
			if (level >= levels.length) {
				ws.send(JSON.stringify({
					type: "congrats",
					value: process.env.GZCTF_FLAG
				}));
				ws.close();
				return;
			}
			goalTimer = 0;
			gameState = JSON.parse(JSON.stringify(levels[level]));
			init();
		}
		ws.send(JSON.stringify({
			type: "ball",
			value: {
				x: gameState.circle.x,
				y: gameState.circle.y,
				moving: gameState.circle.dx + gameState.circle.dy > 0
			}
		}));
	}

	ws.send(JSON.stringify({
		type: "start"
	}));

	function init() {
		ws.send(JSON.stringify({
			type: "colliders",
			value: gameState.rects
		}));
		ws.send(JSON.stringify({
			type: "flag",
			value: gameState.goal
		}));
	}
	init();

	ws.on("message", data => {
		let parsed;
		try {
			parsed = JSON.parse(data.toString?.());
		} catch (e) {}
		if (!parsed) return;
		
		switch (parsed?.type) {
			case "launch":
				if (!parsed?.value) return;
				if (typeof parsed?.value?.dx !== "number") return;
				if (typeof parsed?.value?.dy !== "number") return;
				launchBall(gameState.circle, parsed.value);
			break;
			case "cheat":
				gameState.circle.x = gameState.goal.x;
				gameState.circle.y = gameState.goal.y;
			break;
		}
	});

	ws.on("close", () => {
		clearInterval(interval);
	});
})

app.get("/", (req, res)=>{
	res.sendFile(path.join(__dirname, "public", "index.html"))
});

const WALL_THICKNESS = 30;
const MAX_SPEED = 52;
const DECELERATION = 0.985;
let levels = [{
	goal: { x: 230, y: 420, r: 20 },
	circle: { x: 200, y: 200, dx: 0, dy: 0, r: 12 },
	rects: [
		[150, 500, 1000, WALL_THICKNESS],
		[150, 300, WALL_THICKNESS, 230],
		[150, 300, 800, WALL_THICKNESS],
		[1150, 50, WALL_THICKNESS, 480],
		[150, 50, 1000, WALL_THICKNESS],
		[150, 50, WALL_THICKNESS, 280],
		[400, 50, WALL_THICKNESS, 180],
		[600, 150, WALL_THICKNESS, 150],
		[800, 50, WALL_THICKNESS, 180],
		[500, 400, 450, WALL_THICKNESS]
	]
},{
	goal: { x: 340, y: 425, r: 20 },
	circle: { x: 100, y: 100, dx: 0, dy: 0, r: 12 },
	rects: [
		[50, 50, 1200, WALL_THICKNESS],
		[1200 + WALL_THICKNESS, 50, WALL_THICKNESS, 700 + WALL_THICKNESS],
		[50, 50, WALL_THICKNESS, 700],
		[50, 750, 1200, WALL_THICKNESS],

		[50, 120, 1130, WALL_THICKNESS],
		[1150, 130, WALL_THICKNESS, 580],
		[120, 680, 1050, WALL_THICKNESS],
		[120, 200, WALL_THICKNESS, 500],

		[120, 200, 980, WALL_THICKNESS],
		[1070, 220, WALL_THICKNESS, 400],
		[200, 590, 900, WALL_THICKNESS],
		[200, 270, WALL_THICKNESS, 330],

		[200, 270, 800, WALL_THICKNESS],
		[1000, 270, WALL_THICKNESS, 270],
		[300, 510, 700, WALL_THICKNESS],
		[280, 340, WALL_THICKNESS, 200],

		[280, 330, 670, WALL_THICKNESS],
		[920, 330, WALL_THICKNESS, 140],

		// :3
		[370, 390, 25, 25],
		[370, 440, 25, 25],
		[420, 370, 60, 25],
		[460, 370, 25, 110],
		[420, 415, 60, 25],
		[420, 460, 65, 25],
	]
},{
	goal: { x: 1100, y: 630, r: 20 },
	circle: { x: 250, y: 250, dx: 0, dy: 0, r: 12 },
	rects: [
		[50, 50, 400, WALL_THICKNESS],
		[50, 400, 420, WALL_THICKNESS],
		[50, 50, WALL_THICKNESS, 350],
		[450, 50, WALL_THICKNESS, 380],

		[700, 100, 200, WALL_THICKNESS],
		[700, 700, 500, WALL_THICKNESS],
		[700, 100, WALL_THICKNESS, 600],
		[900, 100, WALL_THICKNESS, 450],
		[900, 530, 300, WALL_THICKNESS],
		[1200, 530, WALL_THICKNESS, 200],
	]
}];

function circlesIntersecting(circle1, circle2) {	
	return Math.sqrt((circle2.x - circle1.x) ** 2 + (circle2.y - circle1.y) ** 2) <= circle1.r + circle2.r;
}

function launchBall(circle, vel) {
	if (circle.dx === 0 && circle.dy === 0) {
			circle.dx = vel.dx;
			circle.dy = vel.dy;
		if (circle.dx > MAX_SPEED) {
			circle.dx = MAX_SPEED;
		} else if (circle.dx < -MAX_SPEED) {
			circle.dx = -MAX_SPEED;
		}
		if (circle.dy > MAX_SPEED) {
			circle.dy = MAX_SPEED;
		} else if (circle.dy < -MAX_SPEED) {
			circle.dy = -MAX_SPEED;
		}
	}
}

function applyVelocity(circle, rects) {
	let initialX = circle.x;
	let initialY = circle.y;

	while (initialX === circle.x && initialY === circle.y &&
		(circle.dy !== 0 || circle.dx !== 0)) {
		circle.x += circle.dx;
		circle.y += circle.dy;

		for (let rect of rects) {
			if (circleRectCollision(circle, rect)) {
				circle.x = initialX;
				circle.y = initialY;

				while (circleRectCollision(circle, rect)) {
					circle.x += (circle.dx / Math.abs(circle.dx)) * circle.r;
					circle.y += (circle.dy / Math.abs(circle.dy)) * circle.r;
				}
			}
		}

		circle.dx = circle.dx * DECELERATION;
		circle.dy = circle.dy * DECELERATION;
		if (Math.abs(circle.dx * DECELERATION) < 0.15 && Math.abs(circle.dy * DECELERATION) < 0.15) {
			circle.dx = 0;
			circle.dy = 0;
		}
	}
}

function circleRectCollision(circle, rect) {
	let closestX = clamp(circle.x, rect[0], rect[0] + rect[2]);
	let closestY = clamp(circle.y, rect[1], rect[1] + rect[3]);

	let distanceX = circle.x - closestX;
	let distanceY = circle.y - closestY;
	let distanceSquared = (distanceX * distanceX) + (distanceY * distanceY);

	if (distanceSquared < (circle.r * circle.r)) {
		let distance = Math.sqrt(distanceSquared);
		let overlap = circle.r - distance;

		if (distance > 0) {
			circle.x += overlap * (distanceX / distance);
			circle.y += overlap * (distanceY / distance);
		}

		let velocityMagnitude = Math.sqrt(circle.dx * circle.dx + circle.dy * circle.dy);
		if (velocityMagnitude > 0) {
			let normalX = distanceX / distance;
			let normalY = distanceY / distance;
			let dotProduct = circle.dx * normalX + circle.dy * normalY;

			if (dotProduct < 0) {
				circle.dx -= 2 * dotProduct * normalX;
				circle.dy -= 2 * dotProduct * normalY;
			}
		}
		return true;
	}
	return false;
}

function clamp(value, min, max) {
	return Math.min(Math.max(value, min), max);
}

app.use(express.static(path.join(__dirname, "public")))

server.listen(8080);
