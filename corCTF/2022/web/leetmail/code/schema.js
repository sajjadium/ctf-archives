const userSchema = {
	body: {
		type: 'object',
		properties: {
			username: { 
                type: 'string', 
                maxLength: 20,
                pattern: "^[a-zA-Z0-9]+$"
            },
			password: { type: 'string', maxLength: 30 }
		},
		required: ['username', 'password']
	}
};

export { userSchema }
