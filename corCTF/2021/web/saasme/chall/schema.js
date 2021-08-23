module.exports = {
	body: {
		type: 'object',
		required: ['url'],
		properties: {
			url: {
				type: 'string',
				maxLength: 200,
				minLength: 1
			}
		}
	}
}