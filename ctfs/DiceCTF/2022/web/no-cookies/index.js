const crypto = require('crypto');

const sha = (data) => {
  const hash = crypto.createHash('sha256');
  hash.update(data);
  return hash.digest('hex');
};

const database = require('better-sqlite3')('db.sqlite3');

const db = {
  prepare: (query, params) => {
    if (params)
      for (const [key, value] of Object.entries(params)) {
        const clean = value.replace(/['$]/g, '');
        query = query.replaceAll(`:${key}`, `'${clean}'`);
      }
    return query;
  },
  get: (query, params) => {
    const prepared = db.prepare(query, params);
    try {
      return database.prepare(prepared).get();
    } catch {}
  },
  run: (query, params) => {
    const prepared = db.prepare(query, params);
    try {
      return database.prepare(prepared).run();
    } catch {}
  },
};

db.run(`
  CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT
  );
`);

db.run(`
  CREATE TABLE IF NOT EXISTS notes(
    id TEXT,
    username TEXT,
    note TEXT,
    mode TEXT,
    views INTEGER
  );
`);

const app = require('express')();

app.use(require('body-parser').json());

app.use(
  require('serve-static')('public', {
    extensions: ['html'],
  })
);

app.post('/register', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) return res.json({});
  if (db.get('SELECT * FROM users WHERE username = :username', { username }))
    return res.json({});

  const hash = sha(password);
  db.run('INSERT INTO users VALUES (:username, :hash)', { username, hash });
  res.json({ success: true });
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) return res.json({});
  const hash = sha(password);
  const user = db.get(
    'SELECT * FROM users WHERE username = :username AND password = :hash',
    {
      username,
      hash,
    }
  );
  if (!user) return res.json({});
  res.json({ success: true });
});

app.post('/create', (req, res) => {
  const { username, password, note, mode } = req.body;
  if (!username || !password || !note || !mode) return res.json({});

  const hash = sha(password);
  const user = db.get(
    'SELECT * FROM users WHERE username = :username AND password = :hash',
    {
      username,
      hash,
    }
  );
  if (!user) return res.json({});

  const id = crypto.randomBytes(16).toString('hex');
  db.run('INSERT INTO notes VALUES (:id, :username, :note, :mode, 0)', {
    id,
    username,
    note: note.replace(/[<>]/g, ''),
    mode,
  });

  res.json({ id });
});

app.post('/view', (req, res) => {
  const { username, password, id } = req.body;
  if (!username || !password || !id) return res.json({});

  const hash = sha(password);
  const user = db.get(
    'SELECT * FROM users WHERE username = :username AND password = :hash',
    {
      username,
      hash,
    }
  );
  if (!user) return res.json({});

  const { note, mode, views } = db.get(
    'SELECT note, mode, views FROM notes WHERE id = :id',
    {
      id,
    }
  );
  if (!note || !mode) return res.json({});

  db.run('UPDATE notes SET views = views + 1 WHERE id = :id', { id });

  res.json({ note, mode, views });
});

app.listen(3000);
