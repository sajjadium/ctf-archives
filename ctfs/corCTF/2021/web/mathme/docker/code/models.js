const crypto = require('crypto');
const bcrypt = require('bcryptjs');
const { Sequelize, Model, DataTypes } = require('sequelize');

const sequelize = new Sequelize({
	dialect: 'sqlite',
	storage: 'database.sqlite3',
	logging: console.log
});

class User extends Model {}
User.init({
	username: DataTypes.STRING,
	password: DataTypes.STRING
}, { sequelize, modelName: 'user' });

class Note extends Model {}
Note.init({
	title: DataTypes.STRING,
	data: DataTypes.TEXT
}, { sequelize, modelName: 'note' });

User.hasMany(Note)
Note.belongsTo(User);

sequelize.sync();

User.count({ where: { username: 'admin' } }).then(count => {
	if (count === 0) {
		return User.create({
			id: 1,
			username: 'admin',
			password: bcrypt.hashSync(crypto.randomBytes(32).toString('base64'), 12)
		})
	} else {
		return Promise.resolve();
	}
}).then(user => {
	if (user) {
		console.log('Created admin user');
	}
})

module.exports = { User, Note }