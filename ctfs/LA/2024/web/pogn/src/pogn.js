// basic number ops
const min = (a, b) => (a < b) ? a : b;
const max = (a, b) => (a > b) ? a : b;
const clamp = (x, low, high) => min(max(x, low), high);

const Msg = {
  GAME_UPDATE: 0,
  CLIENT_UPDATE: 1,
  GAME_END: 2
};

const serverToViewport = ([x, y]) => [
  x * innerWidth / 100,
  (y + 30) * 0.5 * innerHeight / 30
];

const viewportToServer = ([x, y]) => [
  x * 100 / innerWidth,
  y * 30 / (0.5 * innerHeight) - 30
];

let ballPos = [50, 0];
let userPos = [0, innerHeight / 2];
let serverPos = [100, 0];

const wsurl = new URL(location);
wsurl.protocol = location.protocol == 'http:' ? 'ws' : 'wss';
wsurl.pathname = '/ws';

const ws = new WebSocket(wsurl);

ws.addEventListener('open', () => {
  ws.addEventListener('message', (e) => {
    const msg = JSON.parse(e.data);
    switch (msg[0]) {
      case Msg.GAME_UPDATE:
        ballPos = serverToViewport(msg[1][0]);
        serverPos = serverToViewport(msg[1][1]);
        updateFromRemote();
        break;
      case Msg.GAME_END:
        alert(msg[1]);
        break;
    }
  })

  const interval = setInterval(() => {
    if (!moved) return;
    ws.send(JSON.stringify([
      Msg.CLIENT_UPDATE,
      [ userPos, v ]
    ]));
  }, 50);

  ws.addEventListener('close', () => clearInterval(interval));
});

const $ = x => document.querySelector(x);

const userPaddle = $('.user.paddle');
const serverPaddle = $('.server.paddle');
const ball = $('.ball');

let moved = false;
let p_x = 0;
let p_y = 0;
let v = [0, 0];
window.addEventListener('mousemove', (e) => {
  moved = true;
  const x = clamp(e.clientX, 0, innerWidth / 2 - 48);
  const y = e.clientY;
  userPaddle.style = `--x: ${x}px; --y: ${y}px`;
  userPos = viewportToServer([ x, y ]);
  v = viewportToServer([0.01 * (x - p_x), 0.01 * (y - p_y)]);
  p_x = x;
  p_y = y;
});

const updateFromRemote = () => {
  ball.style = `--x: ${ballPos[0]}px; --y: ${ballPos[1]}px`;
  serverPaddle.style = `--x: ${serverPos[0]}px; --y: ${serverPos[1]}px`;
};
