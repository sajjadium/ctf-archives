const fs = require('fs');
const http = require('http');
const path = require('path');

const flag = fs.readFileSync(path.join(__dirname, 'flag.txt')).toString().trim();

const types = new Map([
  ['.html', 'text/html'],
  ['.css', 'text/css'],
  ['.js', 'application/javascript'],
  ['.png', 'image/png'],
]);

const errors = new Set(['ENOENT', 'EISDIR', 'ENOTDIR', 'ENAMETOOLONG']);

http.ServerResponse.prototype.json = function (obj) {
  if (!this.getHeader('content-type')) {
    this.setHeader('content-type', 'application/json');
  }
  this.end(JSON.stringify(obj));
}

const state = { clicks: 0 };
const routes = {
  clicks: async (_req, res) => {
    if (state.clicks === Infinity) res.json({ flag, ...state });
    else res.json(state);
  },
  click: async (_req, res) => {
    state.clicks++;
    res.end();
  },
  static: async (req, res) => {
    const regex = /\.\.\//g;
    const clean = (path) => {
      const replaced = path.replace('../', '');
      if (regex.test(path)) {
        return clean(replaced);
      }
      return replaced;
    };

    const location = [__dirname, 'static', clean(req.url)];
    if (location[2].endsWith('/')) location.push('index.html');
    const file = path.join(...location);

    let data;
    try {
      data = await fs.promises.readFile(file);
    } catch (e) {
      if (errors.has(e.code)) {
        res.statusCode = 404;
        res.end('not found');
        return;
      } else if (e.code === 'EACCES') {
        res.statusCode = 403;
        res.end('forbidden');
        return;
      } else {
        res.statusCode = 500;
        res.end('error');
        return;
      }
    }

    const type = types.get(path.extname(file)) ?? 'text/plain';
    res.setHeader('content-type', type);
    res.end(data);
  },
};

const router = new Map([
  ['/click', routes.click],
  ['/clicks', routes.clicks],
]);
const server = http.createServer(async (req, res) => {
  try {
    const route = router.get(req.url) ?? routes.static;
    return route(req, res);
  } catch (e) {
    res.statusCode = 500;
    res.end('something went wrong.');
  }
});

server.listen(3000, () => {
  console.log('listening on port 3000');
});
