import sqlite3 from 'sqlite3';

const usersQuery = `
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    pid VARCHAR(255) NOT NULL,
    birthdate DATE NOT NULL
);`

const vehiclesQuery = `
CREATE TABLE IF NOT EXISTS vehicles (
    vin TEXT PRIMARY KEY NOT NULL,
    plate VARCHAR(255),
    uid INTEGER NOT NULL
);`

export default class DBFactory {
    static db;
    static async getDB() {
        if (!DBFactory.db) {
            DBFactory.db = new DB();
            await DBFactory.db.migrate();
        }
        return DBFactory.db;
    }
}

class DB {
    db;
    constructor() {}

    async migrate() {
        this.db = new sqlite3.Database("sqlite3.db")
        await this.db.run(usersQuery);
        await this.db.run(vehiclesQuery);
        return;
    }

    async createUser(name, pid, birthdate) {
        const res = await this._insert(`INSERT INTO users (name,pid,birthdate) VALUES (?,?,?);`, [name, pid, birthdate]);
        return res;
    }

    async createVehicle(vin, uid, plate) {
        const res = await this._insert(`INSERT INTO vehicles (vin, uid, plate) VALUES (?,?,?);`, [vin, uid, plate]);
        return res;
    }

    async getVehicles(uid) {
        const results = await this._all(`SELECT * FROM vehicles WHERE uid = ?`, [uid]);
        return results;
    }

    async getUserByVIN(vin) {
        const query = `SELECT * FROM users WHERE id = (SELECT uid FROM vehicles WHERE vin = ?)`;
        const res = await this._get(query, [vin]);
        return res;
    }

    async getVehicleByVIN(vin) {
        const query = `SELECT * FROM vehicles WHERE vin = ?`;
        const res = await this._get(query, [vin]);
        return res;
    }

    async deleteVehicle(vin) {
        await this.db.run(`DELETE FROM vehicles WHERE vin = ?`, [vin]);
        return;
    }

    async deleteUser(uid) {
        await this.db.run(`DELETE FROM users WHERE id = ?`, [uid]);
        return;
    }

    async canRegisterVehicle(vin) {
        const query = `SELECT COUNT(*) as count FROM vehicles WHERE vin = ?`;
        const res = await this._get(query, [vin]);
        return res.count === 0;
    }

    async getLicensePlates() {
        const results = await this._all(`SELECT DISTINCT plate FROM vehicles`);
        const refinedResults = results.map(result => result.plate);
        return refinedResults;
    }

    _get(query, params) {
        return new Promise((resolve, reject) => {
            this.db.get(query, params, (err, row) => {
                if (err) {
                    reject(err);
                }
                resolve(row);
            });
        });
    }

    _all(query, params) {
        return new Promise((resolve, reject) => {
            this.db.all(query, params, (err, rows) => {
                if (err) {
                    reject(err);
                }
                resolve(rows);
            });
        });
    }

    _insert(query, params) {
        return new Promise((resolve, reject) => {
            this.db.run(query, params, function(err) {
                if (err) {
                    reject(err);
                }
                resolve(this.lastID);
            });
        });
    }
}