// util functions for snake

const WIDTH = 600;
const HEIGHT = WIDTH;

let canvas;
let ctx;
let pelletAmount = 0;
let snakeX = WIDTH / 2;
let snakeY = HEIGHT / 2;
let pelletX = Math.random() * WIDTH;
let pelletY = Math.random() * HEIGHT;
let gameOver = false;

// unit is radians
let direction = 0;

function initialize() {
  canvas = document.getElementById('canvas');
  ctx = canvas.getContext('2d');

  // background
  drawBG();

  // le snek
  drawSnake();

  // le pellet
  drawPellet();
}

function drawBG() {
  ctx.fillStyle = 'green';
  ctx.fillRect(0, 0, WIDTH, HEIGHT);
}

function drawPellet() {
  ctx.beginPath();
  ctx.fillStyle = 'orange';
  ctx.arc(pelletX, pelletY, WIDTH / 10 / 2, 0, 2 * Math.PI);
  ctx.fill();
}

function drawSnake() {
  ctx.beginPath();
  ctx.fillStyle = 'blue';
  ctx.arc(snakeX, snakeY, WIDTH / 10 / 2, 0, 2 * Math.PI);
  ctx.fill();
}

function tick() {
  if (gameOver) {
    clearTimeout(TICKER);
    const name = prompt('what\'s your username? (for the share)')
    fetch('/record', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: name,
        score: pelletAmount
      })
    }).then(res => {
      if (res.redirected) {
        window.location.href = res.url;
      } else {
        res.text().then(text => {
          alert(`reporting score failed with: ${text}`)
        })
      }      
    });  
    return;
  }

  // hey did the snake touch the pellet
  if (Math.sqrt(Math.pow(pelletX - snakeX, 2) + Math.pow(pelletY - snakeY, 2)) <= (WIDTH / 10)) {
    pelletAmount += 1;
    pelletX = Math.random() * WIDTH;
    pelletY = Math.random() * HEIGHT;
  }

  // maybe I should get a better formula for this...
  const speed = (pelletAmount + 1) * 5;
  const dx = speed * Math.cos(direction);
  const dy = speed * Math.sin(direction);

  // clear old snek
  drawBG();
  drawPellet();

  snakeX += dx;
  snakeY += dy;
  drawSnake();

  if (snakeX <= (WIDTH / 10 / 2) || snakeY <= (WIDTH / 10 / 2) || snakeX >= (WIDTH - WIDTH / 10 / 2) || snakeY >= (WIDTH - WIDTH / 10 / 2)) {
    gameOver = true;
  }
}

// btw no these race conditions is not the challenge stop looking
let rightPressed = false;
let leftPressed = false;
let upPressed = false;
let downPressed = false;

window.onkeydown = evt => {
  // up
  if (evt.keyCode == 38) {
    upPressed = true;
  }
  // down
  else if (evt.keyCode == 40) {
    downPressed = true;
  }
  // left
  else if (evt.keyCode == 37) {
    leftPressed = true;
  }
  // right
  else if (evt.keyCode == 39) {
    rightPressed = true;
  }

  setDirection();
}

window.onkeyup = evt => {
  // up
  if (evt.keyCode == 38) {
    upPressed = false;
  }
  // down
  else if (evt.keyCode == 40) {
    downPressed = false;
  }
  // left
  else if (evt.keyCode == 37) {
    leftPressed = false;
  }
  // right
  else if (evt.keyCode == 39) {
    rightPressed = false;
  }

  setDirection();
}

function addDirections(one, two) {
  // math is hard :(
  if ((one <= (-Math.PI / 2) && two >= (Math.PI / 2))
    || (two <= (-Math.PI / 2) && one >= (Math.PI / 2))) {
      return (one + two) / 2 + Math.PI;
    } else {
      return (one + two) / 2;
    }
}

function setDirection() {
  const upDir = upDirection();
  const rightDir = rightDirection();

  if (upDir === undefined && rightDir === undefined) {
    return;
  } else if (upDir === undefined) {
    direction = rightDir;
  } else if (rightDir === undefined) {
    direction = upDir;
  } else {
    direction = addDirections(upDir, rightDir);
  }
}

// returns the angle only taking upwards / downwards into account
function upDirection() {
  if ((!upPressed && !downPressed) || (upPressed && downPressed)) {
    return undefined;
  } else {
    if (upPressed) {
      return -Math.PI / 2;
    } else {
      return Math.PI / 2;
    }
  }
}

// same but for left / right
function rightDirection() {
  if ((!leftPressed && !rightPressed) || (leftPressed && rightPressed)) {
    return undefined;
  } else {
    if (leftPressed) {
      return Math.PI;
    } else {
      return 0;
    }
  }
}
