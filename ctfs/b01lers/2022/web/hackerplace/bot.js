const WebSocket = require('ws');
const PNG = require('pngjs').PNG;
const fs = require('fs');
const jwt = require('jsonwebtoken');
const axios = require('axios');

let redPaletteIdx = 1;
let darkRedPaletteIdx = 2;

let offsetX;
let offsetY;
let imgWidth;
let imgHeight;
let image = [];

let secret = 'seeeeecret';
axios.defaults.baseURL = `http://place:3000/stats/`;
axios.defaults.headers.common['Secret'] = secret;
let cooldown = 1;
let palette = ['white', 'red', 'darkred', 'deeppink', 'gold', 'goldenrod', 'lime', 'seagreen', 'cyan', 'cornflowerblue', 'darkviolet', 'grey', 'dimgrey', 'black'];

fs.createReadStream('pixel.png').pipe(new PNG()).on('parsed', function () {
	offsetX = 200 - Math.floor(this.width / 2);
	offsetY = 200 - Math.floor(this.height / 2);
	imgWidth = this.width;
	imgHeight = this.height;
	for (let y = 0; y < this.height; y++) {
		for (let x = 0; x < this.width; x++) {
			let idx = (this.width * y + x) << 2;
			if (this.data[idx] == 255) {
				image.push(redPaletteIdx);
			} else if (this.data[idx] == 128) {
				image.push(darkRedPaletteIdx);
			} else {
				image.push(-1);
			}
		}
	}
});

function fixImage() {
	for (let y = offsetY; y < offsetY + imgHeight; y++) {
		for (let x = offsetX; x < offsetX + imgWidth; x++) {
			let tx = x - offsetX;
			let ty = y - offsetY;
			if (image[ty * imgWidth + tx] != -1 && canvas[y * 400 + x] != image[ty * imgWidth + tx]) {
				let color = palette[image[ty*imgWidth + tx]];
				let packet = '';
				packet += leftPad(String(x), ' ', 3);
				packet += leftPad(String(y), ' ', 3);
				packet += '"' + color + '"';
				conn.send(packet);
				canvas[y * 400 + x] = image[ty * imgWidth + tx];
				return;
			}
		}	
	}
}

let conn = new WebSocket('ws://place:3000/', {
	headers: {
		'Cookie': `token=${jwt.sign({ cooldown }, secret, { algorithm: 'HS256' })}`
	}
});
conn.onopen = function () {
	console.log('Bot connected to hacker/place');
	setInterval(fixImage, cooldown * 1050);
}

function leftPad(string, pad, length) {
    while (string.length < length) {
        string = pad + string;
    }
    return string;
}
let canvas = null;
conn.on('message', function (data) {
	let type = data.readUint8();
	switch (type) {
		case 1:
			canvas = new Uint8Array(400 * 400);
			for (let y = 0; y < 400; y++) {
				for (let x = 0; x < 400; x++) {
					canvas[y * 400 + x] = data[y * 400 + x + 1];
				}
			}
			break;
		case 2:
			try {
				let str = data.toString();
				let x = JSON.parse(str.slice(1, 4));
				let y = JSON.parse(str.slice(4, 7));
				let color = JSON.parse(str.slice(7));
				canvas[y * 400 + x] = palette.indexOf(color);
			} catch (err) {
				console.error(err);
			}
			break;
		case 3:
			break;
		case 4:
			try {
				let str = data.toString();
				let x = JSON.parse(str.slice(1, 4));
				let y = JSON.parse(str.slice(4, 7));
				let color = JSON.parse(str.slice(7));
				try {
					color = color.replace('://', '')
				} catch (err) {
					//
				}
				console.log(`Logging opposing pixel placed at ${x}, ${y} with color ${color}`);
				axios(color, {
					method: 'post',
					data: { x, y }
				}).catch((err) => {});
			} catch (err) {
				console.error('error');
				// console.error(err);
			}
			break;
	}
})
