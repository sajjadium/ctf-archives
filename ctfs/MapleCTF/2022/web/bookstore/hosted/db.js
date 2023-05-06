import mysql from 'mysql'
const LIMIT = 500;

export default class DB {
    constructor() {
        this.adminDB = mysql.createConnection({
            connectionLimit: 100,
            host: process.env.DB_HOST || 'localhost',
            user: process.env.DB_ADMIN_USER || 'root',
            password: process.env.DB_ADMIN_PASS || 'Rooted123!',
            database: process.env.DB_NAME || 'bookstore',
        });

        this.db = mysql.createPool({
            connectionLimit: 100,
            host: process.env.DB_HOST || 'localhost',
            user: process.env.DB_USER || 'player',
            password: process.env.DB_PASS || 'Player123!',
            database: process.env.DB_NAME || 'bookstore',
        });
    }

    register(username, password) {
        return new Promise((resolve, reject) => {
            this.adminDB.query(`INSERT INTO users(username, password) VALUES('${username}', '${password}')`, (err) => {
                if (err) {
                    console.log(err)
                    reject(err);
                } else {
                    resolve(null);
                }
            })
        })
    }

    getUser(username, password, callback) {
        const query = `
        SELECT * FROM users WHERE username = '${username}' AND password = '${password}';
        `;
        this.db.query(query, (err, user) => {
            callback(user);
        });
    }

    getBooks() {
        const query = `SELECT id, title, author, price FROM books;`;
        return new Promise((resolve, reject) => {
            this.db.query(query, (error, rows) => {
                if (error) {
                    reject(error);
                } else {
                    resolve(rows);
                }
            }).on('error', (err) => {
                reject(err);
            })
        })
    }


    insertEmail(email, book_id) {
        const query = `INSERT INTO requests(email, book_id) VALUES('${email}', '${book_id}');`;
        return new Promise((resolve, reject) => {
            this.db.query(query, (error) => {
                if (error != null) {
                    reject(error);
                } else {
                    resolve(null);
                }
            })
        })
    }

    purge() {
        // disappoints users
        const countQuery = "SELECT COUNT(*) FROM requests;"
        return new Promise((resolve, reject) => {
            this.adminDB.query(countQuery, (error, row) => {
                if (error != null) {
                    reject(error);
                } else {
                    if (row.COUNT > LIMIT) {
                        const deleteQuery = `DELETE FROM requests;`
                        this.db.query(deleteQuery, (err) => {
                            if (err != null) {
                                reject(err);
                            } else {
                                resolve(null);
                            }
                        })
                    }
                }
            })
        })
    }
}