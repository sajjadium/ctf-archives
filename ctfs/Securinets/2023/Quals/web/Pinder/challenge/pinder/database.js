const util = require('util');
const mysql = require('mysql');

class Database {
    constructor(user, password, database) {
        this.db = mysql.createConnection({
            host: 'localhost',
            user: user,
            password: password,
            database: database,
            stringifyObjects: true
        });
        this.query = util.promisify(this.db.query).bind(this.db);
    }

    connect() {
        this.db.connect();
    }

    async userExists(username) {
        const result = await this.query('SELECT * FROM users WHERE username = ?', [username]);
        return result.length === 1;
    }

    async registerUser(username, password, secret) {
        const result = await this.query('INSERT INTO users (username, password) VALUES (?, ?)', [username, password]);
        return result;
    }

    async loginUser(username, password) {
        const result = await this.query('SELECT * FROM users WHERE username = ? AND password = ?', [username, password]);
        return result.length === 1 ? result[0] : false;
    }

    async createProfile(userId, first_name,last_name,profile_picture_link,is_public=false) {
        const result = await this.query('INSERT INTO profile (user_id, first_name,last_name,profile_picture_link,is_public) VALUES (?, ?, ?, ?, ?)',
            [userId, first_name, last_name,profile_picture_link,is_public]);
        return result;
    }

    async getProfile(userId) {
        const result = await this.query('SELECT * FROM profile WHERE user_id = ? and is_public=1', [userId]);
        return result;
    }

    async getAllPublicProfiles() {
        const result = await this.query('SELECT * FROM profile WHERE is_public = ?', [true]);
        return result;
    }

    async getAllProfiles() {
        const result = await this.query('SELECT * from profile' );
        return result;
    }

    async searchProfile(search_query) {
        const result = await this.query("SELECT * FROM profile WHERE first_name LIKE ?", [search_query+'%'])
        return result;
    }

}

module.exports=Database
