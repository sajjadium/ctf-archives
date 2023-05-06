const Busboy = require('busboy');
const crypto = require('crypto');
const dns = require('dns');

// middleware using busboy to parse multipart forms
const multipartFormParser = async (req, _res, next) => {
  if (!req.is('multipart/form-data')) return next();
  const formData = new Map();

  const busboy = new Busboy({ headers: req.headers });
  const finish = new Promise((resolve) => {
    busboy.on('finish', resolve);
  });

  // on file, read entire file and put into map
  busboy.on('file', async (key, file) => {
    const data = [];
    const end = new Promise((resolve) => {
      file.on('end', resolve);
    });

    file.on('data', (chunk) => data.push(chunk));
    await end;

    if (!formData.has(key))
      formData.set(key, {
        value: Buffer.concat(data),
        type: 'file',
      });
  });

  // put fields in map too
  busboy.on('field', (key, value) =>
    formData.set(key, {
      value,
      type: 'field',
    })
  );

  req.pipe(busboy);

  await finish;
  req.body = formData;

  next();
};

// scuffed ""database""
class Database {
  constructor() {
    // username -> info
    this.users = new Map();
    // token -> username
    this.tokens = new Map();
  }

  register(username, info) {
    this.users.set(username, info);
  }

  login(username) {
    const token = crypto.randomUUID();
    this.tokens.set(token, username);
    return token;
  }

  getUsername(token) {
    return this.tokens.get(token);
  }

  getInfo(username) {
    return this.users.get(username);
  }
}

const validateURL = async (protocol, host) => {
  if (protocol !== 'http:' && protocol !== 'https:') return [false];
  if (typeof host !== 'string') return [false];
  let ip = host;

  // if it's not just numbers and dots, it's not ipv4 and needs resolution
  if (/[^\d\.]/.test(host)) {
    try {
      ip = await new Promise((resolve, reject) => {
        dns.lookup(host, { family: 4 }, (err, address, family) => {
          if (err) return reject(err);
          if (family === 4) return resolve(address);
          reject(new Error('Invalid ip.'));
        });
      });
    } catch {
      return [false];
    }
  }

  if (ip.startsWith('0')) return [false];
  if (ip.startsWith('127')) return [false];
  if (ip.startsWith('10.')) return [false];

  return [true, ip];
};

module.exports = Database;

module.exports = {
  multipartFormParser,
  validateURL,
  Database,
};
