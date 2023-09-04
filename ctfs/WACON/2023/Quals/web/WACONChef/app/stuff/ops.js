const crypto = require('crypto');
const bcrypt = require('bcrypt');

const bcryptSalt = bcrypt.genSaltSync(5);
['sha1','sha256','sha512','md5'].forEach(algo=>{
	exports[algo] = e=>crypto.createHash(algo).update(e).digest('hex');
});
exports.bcrypt = e=>bcrypt.hashSync(e,bcryptSalt);
exports.base64_encode = e=>e.toString('base64');
exports.base64_decode = e=>atob(e);
exports.hex_encode = e=>e.toString('hex');
exports.hex_decode = e=>Buffer.from(e+'','hex');
exports.URL_encode = e=>(
	e.toString().split('').map(e=>'%'+e.charCodeAt(0).toString(16)).join('')
);
exports.URL_decode = e=>(
	e.toString().replaceAll(/%[a-z0-9]{2}/g,e=>(
		String.fromCharCode(parseInt(e.slice(1),16))
	))
);
exports.html_encode = e=>(
	e.toString().split('').map(e=>`&#x${e.charCodeAt(0).toString(16)};`).join('')
);
exports.html_decode = e=>(
	e.toString().replaceAll(/&#x[a-z0-9]{2};/g,e=>(
		String.fromCharCode(parseInt(e.slice(3,5),16))
	))
);
exports.base32_encode = e=>{
	let alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
	let bits = 0;
	let value = 0;
	let output = '';

	for (let i = 0; i < e.byteLength; i++) {
		value = (value << 8) | e[i];
		bits += 8;
		while (bits >= 5) {
		  output += alphabet[(value >>> (bits - 5)) & 31];
		  bits -= 5;
		}
	}

	if (bits > 0) {
		output += alphabet[(value << (5 - bits)) & 31];
	}

	while ((output.length % 8) !== 0) {
	  output += '=';
	}

	return output;
}
exports.base32_decode = e=>{
	let alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
	let input = e.toString().replace(/=+$/, '');
	let length = input.length;
	let bits = 0;
	let value = 0;
	let index = 0;
	let output = new Uint8Array((length * 5 / 8) | 0);

	for (var i = 0; i < length; i++) {
		value = (value << 5) | alphabet.indexOf(input[i]);
		bits += 5;
		if (bits >= 8) {
			output[index++] = (value >>> (bits - 8)) & 255;
			bits -= 8;
		}
	}

	return Buffer.from(output);
}

