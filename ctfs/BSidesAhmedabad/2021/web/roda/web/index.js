const fs = require('fs');
const axios = require('axios');
const express = require('express');
const multer = require('multer');
const mustacheExpress = require('mustache-express');
const Redis = require('ioredis');
const { v4: uuidv4 } = require('uuid');

const RECAPTCHA_SITE_KEY = process.env.RECAPTCHA_SITE_KEY || '[site key is empty]';
const RECAPTCHA_SECRET_KEY = process.env.RECAPTCHA_SECRET_KEY || '[secret key is empty]';
const SECRET = process.env.SECRET || 's3cr3t';
const FLAG = process.env.FLAG || 'Neko{dummy}';
const REDIS_URL = process.env.REDIS_URL || 'redis://127.0.0.1:6379';

const app = express();
app.use(require('cookie-parser')());
app.use('/static', express.static('static'));
app.engine('mustache', mustacheExpress());
app.set('view engine', 'mustache');
app.set('views', __dirname + '/views');

const port = 5000;
const storage = multer.diskStorage({
  destination: './tmp/'
});

const redis = new Redis(REDIS_URL);

let uploadedFiles = {};
let checkedFiles = {};

const ID_TABLE = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
function generateId(n=8) {
  let res = '';
  for (let i = 0; i < n; i++) {
    res += ID_TABLE[Math.random() * ID_TABLE.length | 0];
  }
  return res;
}

// admin only!
function adminRequired(req, res, next) {
  if (!('secret' in req.cookies)) {
    res.status(401).render('error', {
      message: 'Unauthorized'
    });
    return;
  }

  if (req.cookies.secret !== SECRET) {
    res.status(401).render('error', {
      message: 'Unauthorized'
    });
    return;
  }

  next();
}

app.get('/', (req, res) => {
  res.render('index');
});

app.get('/flag', adminRequired, (req, res) => {
  res.send(FLAG);
});

const SIGNATURES = {
  'png': new Uint8Array([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
  'jpg': new Uint8Array([0xff, 0xd8])
};

function compareUint8Arrays(known, input) {
  if (known.length !== input.length) {
  	return false;
  }

  for (let i = 0; i < known.length; i++) {
    if (known[i] !== input[i]) {
      return false;
    }
  }

  return true;
}

function isValidFile(ext, data) {
  // extension should not have special chars
  if (/[^0-9A-Za-z]/.test(ext)) {
    return false;
  }

  // prevent uploading files other than images
  if (!(ext in SIGNATURES)) {
  	return false;
  }

  const signature = SIGNATURES[ext];
  return compareUint8Arrays(signature, data.slice(0, signature.length));
}

const upload = multer({
  storage,
  limits: {
    files: 1,
    fileSize: 100 * 1024
  }
});
app.post('/upload', upload.single('file'), (req, res) => {
  const { file } = req;
  fs.readFile(file.path, (err, data) => {
    const buf = new Uint8Array(data);

    const fileName = file.originalname;
    const ext = fileName.split('.').slice(-1)[0];
  
    // check if the file is safe
    if (isValidFile(ext, buf)) {
      const newFileName = uuidv4() + '.' + ext;
      fs.writeFile('uploads/' + newFileName, buf, (err, data) => {
        let id;
        do {
          id = generateId();
        } while (id in uploadedFiles);

        uploadedFiles[id] = newFileName;
        res.json({
          status: 'success',
          id
        });
      });
    } else {
      res.json({
        status: 'error',
        message: 'Invalid file'
      });
    }
  });
});

// show uploaded contents
const MIME_TYPES = {
  'png': 'image/png',
  'jpg': 'image/jpeg'
};

app.get('/uploads/:fileName', (req, res) => {
  const { fileName } = req.params;
  const path = 'uploads/' + fileName;

  // no path traversal
  res.type('text/html'); // prepare for error messages
  if (/[/\\]|\.\./.test(fileName)) {
    res.status(403).render('error', {
      message: 'No hack'
    });
    return;
  }

  // check if the file exists
  try {
    fs.accessSync(path);
  } catch (e) {
    res.status(404).render('error', {
      message: 'Not found'
    });
    return;
  }

  // send proper Content-Type header
  try {
    const ext = fileName.split('.').slice(-1)[0];
    res.type(MIME_TYPES[ext]);
  } catch {}

  fs.readFile(path, (err, data) => {
    res.send(data);
  });
});

app.get('/:id', (req, res) => {
  const { id } = req.params;

  if (!(id in uploadedFiles)) {
    res.status(404).render('error', {
      message: 'Not found'
    });
    return;
  }

  res.render('file', {
    path: uploadedFiles[id],
    checked: id in checkedFiles,
    siteKey: RECAPTCHA_SITE_KEY,
    id
  });
});

// report image to admin
app.post('/:id/report', async (req, res) => {
  const { id } = req.params;
  const { token } = req.query;
/*
  const params = `?secret=${RECAPTCHA_SECRET_KEY}&response=${encodeURIComponent(token)}`;
  const url = 'https://www.google.com/recaptcha/api/siteverify' + params;
  const result = await axios.get(url);

  if (!result.data.success) {
    res.json({
      status: 'error',
      message: 'reCAPTCHA failed'
    });
    return;
  }
*/
  redis.rpush('query', id);
  redis.llen('query', (err, result) => {
    console.log('[+] reported:', id);
    console.log('[+] length:', result);
    res.json({
      status: 'success',
      length: result
    });
  })
})

// admin only
app.get('/:id/confirm', adminRequired, (req, res) => {
  const { id } = req.params;

  if (id in uploadedFiles) {
    checkedFiles[id] = true;
  }

  res.send('done');
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
