const crypto = require('crypto');

const base64UrlEncode = (str) => {
	return Buffer.from(str)
		.toString('base64')
		.replace(/=*$/g, '')
		.replace(/\+/g, '-')
		.replace(/\//g, '_');
}

const base64UrlDecode = (str) => {
	return Buffer.from(str, 'base64').toString();
}

const algorithms = {
	hs256: (data, secret) => 
		base64UrlEncode(crypto.createHmac('sha256', secret).update(data).digest()),
	hs512: (data, secret) => 
		base64UrlEncode(crypto.createHmac('sha512', secret).update(data).digest()),
}

const stringifyPart = (obj) => {
	return base64UrlEncode(JSON.stringify(obj));
}

const parsePart = (str) => {
	return JSON.parse(base64UrlDecode(str));
}

const createSignature = (header, payload, secret) => {
	const data = `${stringifyPart(header)}.${stringifyPart(payload)}`;
	const signature = algorithms[header.alg.toLowerCase()](data, secret);
	return signature;
}

const parseToken = (token) => {
	const parts = token.split('.');
	if (parts.length !== 3) throw Error('Invalid JWT format');
	
	const [ header, payload, signature ] = parts;
	const parsedHeader = parsePart(header);
	const parsedPayload = parsePart(payload);
	
	return { header: parsedHeader, payload: parsedPayload, signature }
}

const sign = (alg, payload, secret) => {
	const header = {
		typ: 'JWT',
		alg: alg
	}
	
	const signature = createSignature(header, payload, secret);
	
	const token = `${stringifyPart(header)}.${stringifyPart(payload)}.${signature}`;
	return token;
}

const verify = (token, secret) => {
	const { header, payload, signature: expected_signature } = parseToken(token);

	const calculated_signature = createSignature(header, payload, secret);
	
	const calculated_buf = Buffer.from(calculated_signature, 'base64');
	const expected_buf = Buffer.from(expected_signature, 'base64');

	if (Buffer.compare(calculated_buf, expected_buf) !== 0) {
		throw Error('Invalid signature');
	}

	return payload;
}

module.exports = { sign, verify }
