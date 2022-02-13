const sqlite3 = require('sqlite3');
const flag = require('fs').readFileSync('/flag').toString();

class Database {
  constructor(filename) {
    this.db = new sqlite3.Database(filename);

    this.db.serialize(() => {
      this.run('create table members (username text, password text)');
      this.run('create table posts (id text, title text, content text, owner text)');
      this.run('create table flag (flag text)');
      this.run('insert into flag values (?)', [ flag ]);
    });
  }

  run(...params) {
    return new Promise((resolve) => {
      this.db.serialize(() => {
        this.db.run(this.#formatQuery(...params), (_, res) => {
          resolve(res);
        });
      });
    });
  }

  get(...params) {
    return new Promise((resolve) => {
      this.db.serialize(() => {
        this.db.get(this.#formatQuery(...params), (_, res) => {
          resolve(res);
        });
      });
    });
  }

  getAll(...params) {
    return new Promise((resolve) => {
      this.db.serialize(() => {
        this.db.all(this.#formatQuery(...params), (_, res) => {
          resolve(res);
        });
      });
    });
  }

  #formatQuery(sql, params = []) {
    for (const param of params) {
      if (typeof param === 'number') {
        sql = sql.replace('?', param);
      } else if (typeof param === 'string') {
        sql = sql.replace('?', JSON.stringify(param.replace(/["\\]/g, '')));
      } else {
        sql = sql.replace('?', ""); // unreachable
      }
    }
    return sql;
  };
}

const checkParam = (param) => {
  if (typeof param !== 'string' || param.length === 0 || param.length > 256) {
    return false;
  }

  return true;
};

module.exports = {
  Database,
  checkParam,
  md5: require('md5')
};
