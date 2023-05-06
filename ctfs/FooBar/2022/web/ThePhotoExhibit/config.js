const NodeRSA = require('node-rsa');
const uuid = require('uuid');
class Config {
	constructor(env='local'){
		this.KEY = new NodeRSA({b: 512});
		this.KEY.generateKeyPair();
		this.PUBLIC_KEY = this.KEY.exportKey('public')
		this.PRIVATE_KEY = this.KEY.exportKey('private')
		console.log(this.PUBLIC_KEY)
		console.log(this.PRIVATE_KEY)
		this.KEY_COMP = this.KEY.exportKey('components-public');
		this.KID = uuid.v4();
		this.AUTH_PROVIDER = 'http://localhost:3000';
	}
}

module.exports = Config
