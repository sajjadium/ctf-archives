let canvas = document.querySelector('canvas');
let ctx = canvas.getContext('2d', { alpha: false });
canvas.width = 400;
canvas.height = 400;
ctx.fillStyle = '#fff';
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.webkitImageSmoothingEnabled = false;
let ws = new WebSocket(`ws://${location.hostname}:${location.port}/`);

let cooldownDiv = document.getElementById('cooldown');
let cooldownCounter = document.getElementById('cooldown-counter');
ws.onmessage = async function (e) {
    let palette = document.getElementsByClassName('color')
    let data = new Uint8Array(await e.data.arrayBuffer());
    switch (data[0]) {
        case 1:
            for (let y = 0; y < canvas.height; y++) {
                for (let x = 0; x < canvas.width; x++) {
                    ctx.fillStyle = palette[data[y * 400 + x + 1]].id;
                    ctx.fillRect(x, y, 1, 1);
                }
            }
            break;
        case 2:
            let str = String.fromCharCode.apply(null, data);
            let x = JSON.parse(str.slice(1, 4));
            let y = JSON.parse(str.slice(4, 7));
            ctx.fillStyle = JSON.parse(str.slice(7));
            ctx.fillRect(x, y, 1, 1);
            break;
        case 3:
            cooldownDiv.style.display = 'block';
            let cooldown = 10;
            cooldownCounter.innerText = String(cooldown);
            let interval = setInterval(() => {
                cooldown--;
                cooldownCounter.innerText = String(cooldown);
                if (cooldown <= 0) {
                    cooldownDiv.style.display = 'none';
                    clearInterval(interval);
                }
            }, 1000);
            break;
    }
};

function leftPad(string, pad, length) {
    while (string.length < length) {
        string = pad + string;
    }
    return string;
}
canvas.onclick = function (e) {
    let coords = project(e.offsetX, e.offsetY);
    let packet = '';
    packet += leftPad(String(coords[0]), ' ', 3);
    packet += leftPad(String(coords[1]), ' ', 3);
    packet += '"' + paletteElem.id + '"';
    ws.send(packet);
};


let paletteElem = document.getElementById('palette');
function switchPalette(newElem) {
    if (paletteElem != newElem) {
        paletteElem.classList.remove('selected');
    }
    paletteElem = newElem;
    paletteElem.classList.add('selected');
}
switchPalette(document.getElementById('red'));

let clicked = false;
let x = 0;
let y = 0;
let lastMouseX = null;
let lastMouseY = null;

function project(x, y) {
    return [Math.floor(x / zoom), Math.floor(y / zoom)];
}

let zoom = (Math.min(window.innerWidth, window.innerHeight) / canvas.width) * 0.8;
canvas.style.zoom = `${Math.floor(zoom * 100)}%`;

document.body.onwheel = function (e) {
    zoom -= e.deltaY / 100;
    canvas.style.zoom = `${Math.floor(zoom * 100)}%`;
};

document.body.onmousemove = function (e) {
    if (clicked) {
        x += (e.screenX - lastMouseX) / zoom;
        y += (e.screenY - lastMouseY) / zoom;
        lastMouseX = e.screenX;
        lastMouseY = e.screenY;
        canvas.style.transform = `translate(${x}px, ${y}px)`;
    }
};

document.body.onmousedown = function (e) {
    lastMouseX = e.screenX;
    lastMouseY = e.screenY;
    clicked = true;
};

document.body.onmouseup = function () {
    clicked = false;
};
