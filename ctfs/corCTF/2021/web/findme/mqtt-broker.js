const aedes = require('aedes')();
const { createServer } = require('aedes-server-factory');

const httpServer = createServer(aedes, { ws: true });
const port = 8001;

aedes.authorizeSubscribe = (client, sub, callback) => {
	let topic = sub.topic;

	if ((topic.startsWith('messages/') && !topic.startsWith('messages/' + client.id)) || 
		(topic.startsWith('errors/') && !topic.startsWith('errors/' + client.id)) || 
		topic.includes('+') ||
		topic.includes('#')) {
		// MQTT 5.0 not supported, so to provide feedback we need to publish a message :(
		aedes.publish({
			topic: 'errors/' + client.id,
			payload: 'invalid subscribe packet ' + JSON.stringify(sub)
		});

		return callback(new Error('invalid subscribe packet'));
	}


	callback(null, sub);
}

aedes.authorizePublish = (client, packet, callback) => {
	if (!packet.topic.startsWith('messages/')) {
		// MQTT 5.0 not supported, so to provide feedback we need to publish a message :(
		aedes.publish({
			topic: 'errors/' + client.id,
			payload: 'invalid publish packet ' + JSON.stringify(packet)
		});

		return callback(new Error('invalid publish packet'));
	}

	callback(null);
}

httpServer.listen(port);
