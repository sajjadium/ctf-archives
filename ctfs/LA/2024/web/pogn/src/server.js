const express = require('express');
const expressWs = require('express-ws');
const path = require('path');
const fs = require('fs');

const flag = process.env.FLAG || 'lactf{test_flag}';

const app = express();

expressWs(app);

app.use('/assets', express.static(path.join(__dirname, '../assets')));
app.use('/', express.static(__dirname));

app.ws('/ws', (ws, req) => {
  const yMax = 30;
  const collisionDist = 5;
  const Msg = {
    GAME_UPDATE: 0,
    CLIENT_UPDATE: 1,
    GAME_END: 2
  };

  // game state
  let me = [95, 0];    // my paddle position
  let op = [0, 0];     // user's paddle position
  let opV = [0, 0];    // user's paddle velocity
  let ball = [50, 0];  // balls location
  let ballV = [+5, 0]; // balls speed

  // basic number ops
  const min = (a, b) => (a < b) ? a : b;
  const max = (a, b) => (a > b) ? a : b;
  const clamp = (x, low, high) => min(max(x, low), high);

  // vector ops
  const add = ([x1, y1], [x2, y2]) => [x1 + x2, y1 + y2];
  const sub = ([x1, y1], [x2, y2]) => [x1 - x2, y1 - y2];
  const mul = ([x1, y1], k) => [k * x1, k * y1];
  const bmul = ([x1, y1], [x2, y2]) => [x1 * x2, y1 * y2];
  const norm = ([x, y]) => Math.sqrt(x ** 2 + y ** 2);
  const normalize = (v) => mul(v, 1 / norm(v));

  // validation
  const isNumArray = (v) => Array.isArray(v) && v.every(x => typeof x === 'number');

  let prev = Date.now();
  const interval = setInterval(() => {
    const dt = (Date.now() - prev) / 100;
    prev = Date.now();

    // move server's paddle to be same y as the ball
    me[1] = ball[1];

    // give ball some movement if it stagnates
    if (Math.abs(ballV[0]) < 0.5) {
      ballV[0] = Math.random() * 2;
    }

    // collision with user's paddle
    if (norm(sub(op, ball)) < collisionDist) {
      ballV = add(opV, mul(normalize(sub(ball, op)), 1 / norm(ballV)));
    }

    // collision with server's paddle
    if (norm(sub(me, ball)) < collisionDist) {
      ballV = add([-3, 0], mul(normalize(sub(ball, me)), 1 / norm(ballV)));
    }

    // update ball position
    ball[0] += ballV[0] * dt;
    ball[1] += ballV[1] * dt;

    // wall bouncing
    if (ball[1] < -yMax || ball[1] > yMax) {
      ball[1] = clamp(ball[1], -yMax, yMax);
      ballV[1] *= -1;
    }

    // check if there has been a winner
    // server wins
    if (ball[0] < 0) {
      ws.send(JSON.stringify([
        Msg.GAME_END,
        'oh no you have lost, have you considered getting better'
      ]));
      clearInterval(interval);

    // game still happening
    } else if (ball[0] < 100) {
      ws.send(JSON.stringify([
        Msg.GAME_UPDATE,
        [ball, me]
      ]));

    // user wins
    } else {
      ws.send(JSON.stringify([
        Msg.GAME_END,
        'omg u won, i guess you considered getting better ' +
        'here is a flag: ' + flag,
        [ball, me]
      ]));
      clearInterval(interval);
    }
  }, 50); // roughly 20fps

  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg[0] === Msg.CLIENT_UPDATE) {
      const [ paddle, paddleV ] = msg[1];
      if (!isNumArray(paddle) || !isNumArray(paddleV)) return;
      op = [clamp(paddle[0], 0, 50), paddle[1]];
      opV = mul(normalize(paddleV), 2);
    }
  });

  ws.on('close', () => clearInterval(interval));
});

app.listen(3000);
