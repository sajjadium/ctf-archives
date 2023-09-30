import mongoose from 'mongoose';

let User = new mongoose.Schema({
	username: {
		type: String
	},
	password: {
		type: String
	},
	admin: {
		type: Boolean
	},
	session: {
		type: String
	}
}, {
	collection: 'users'
});

export default mongoose.model('User', User);