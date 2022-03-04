const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');

module.exports = {
	sign(data, privkey, jku, kid) {
		return new Promise((resolve, reject) => {
			try {
				resolve(jwt.sign(data, privkey, {
					algorithm: 'RS256',
					header: { 
						jku: jku,
						kid: kid 
					}
				}));
			} catch (e) {
				reject(e);
			}
		});
	},
	verify(token, pubkey) {
		return new Promise((resolve, reject) => {
			try {
				return resolve(jwt.verify(token, pubkey, { algorithm: 'RS256' }));
			} catch (e) {
				reject(e);
			}
		});
	},
	getHeader(token) {
		return new Promise((resolve, reject) => {
			try {
				return resolve(jwt.decode(token, {
					complete: true
				}).header);
			} catch (e) {
				reject(e);
			}
		});
	},
	getPayload(token) {
		return new Promise((resolve, reject) => {
			try {
				return resolve(jwt.decode(token, {
					complete: true
				}).payload);
			} catch (e) {
				reject(e);
			}
		});
	},
	getPublicKey(jku, kid) {
		return new Promise((resolve, reject) => {
			console.log(jku)
			client = jwksClient({
				jwksUri: jku,
				timeout: 30000,
			});
			client.getSigningKey(kid)
				.then(key => {
					resolve(key.getPublicKey());
				})
				.catch(e => {
					reject(e);
				});
		});
	}
};
