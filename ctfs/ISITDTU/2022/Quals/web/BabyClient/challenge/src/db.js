const sqlite = require('sqlite-async');

class Database {
    constructor(db_file) {
        this.db_file = db_file;
        this.db = undefined;
    }
    
    async connect() {
        this.db = await sqlite.open(this.db_file);
    }

    async migrate() {
        return this.db.exec(`
            PRAGMA case_sensitive_like=ON; 

            DROP TABLE IF EXISTS userEntries;

            CREATE TABLE IF NOT EXISTS userEntries (
                id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                title       VARCHAR(255) NOT NULL UNIQUE,
                url         VARCHAR(255) NOT NULL,
                approved    BOOLEAN NOT NULL
            );

            INSERT INTO userEntries (title, url, approved) VALUES ("Welcome DTU", "https://duytan.edu.vn", 1);
            INSERT INTO userEntries (title, url, approved) VALUES ("Naruto", "https://www.youtube.com/hashtag/naruto", 1);
            INSERT INTO userEntries (title, url, approved) VALUES ("ISITDTU{test_123_abc}","https://ctf.isitdtu.com/", 0);
        `);
    }

    async getEntry(query, approved=1) {
        return new Promise(async (resolve, reject) => {
            try {
                let stmt = await this.db.prepare("SELECT * FROM userEntries WHERE title LIKE ? AND approved = ?");
                resolve(await stmt.all(query, approved));
            } catch(e) {
                console.log(e);
                reject(e);
            }
        });
    }

}

module.exports = Database;