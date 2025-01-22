import express from 'express';
import fs from 'fs';
import path from 'path';
import bodyParser from 'body-parser';
import chalk from 'chalk';
import { fileURLToPath } from 'url';
import { Worker } from 'worker_threads';
import { resolve } from 'path';

const app = express();
const PORT = process.env.PORT || 3000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PREVIEW_LENGTH = 100;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');

const CODE_SAMPLES_DIR = path.join(__dirname, 'code_samples');
const LANG_MAP = {
  '.js': 'JavaScript',
  '.py': 'Python',
  '.java': 'Java',
  '.cpp': 'C++',
  '.c': 'C',
  '.cs': 'C#',
  '.rb': 'Ruby',
  '.php': 'PHP',
  '.kt': 'Kotlin',
  '.rs': 'Rust',
  '.go': 'Go',
  '.swift': 'Swift',
  '.lua': 'Lua',
  '.scala': 'Scala',
  '.ex': 'Elixir',
  '.hs': 'Haskell',
  '.sh': 'Bash',
  '.ts': 'TypeScript',
  '.pl': 'Perl',
  '.r': 'R',
};
let filesIndex = {};

function initializeFiles() {
  const files = fs.readdirSync(CODE_SAMPLES_DIR);
  files.forEach(file => {
    filesIndex[file] = {
      visible: file !== 'flag.txt',
      path: path.join(CODE_SAMPLES_DIR, file),
      name: file,
      language: LANG_MAP[path.extname(file)] || null
    };
  });
  console.log(chalk.green('Initialized file index.'));
}

function runSearchWorker(workerData, timeout = 5000) {
  return new Promise((resolvePromise, rejectPromise) => {
    const worker = new Worker(resolve(__dirname, 'searchWorker.js'), {
      workerData
    });

    worker.on('message', resolvePromise);
    worker.on('error', rejectPromise);
    worker.on('exit', (code) => {
      if (code !== 0)
        resolvePromise({ results: [] });
    });

    const timer = setTimeout(() => {
      worker.terminate().then(() => {
        resolvePromise({ results: [] });
      });
    }, timeout);

    worker.on('message', () => clearTimeout(timer));
    worker.on('error', () => clearTimeout(timer));
    worker.on('exit', () => clearTimeout(timer));
  });
}

app.get('/', (req, res) => res.render('index'));

app.post('/search', async (req, res) => {
  const query = req.body.query.trim();
  const language = req.body.language;
  let searchRegex = null;
  let searchTerm = '';

  if (query.startsWith('/') && query.endsWith('/')) {
    const regexPattern = query.slice(1, -1);
    try {
      searchRegex = new RegExp(regexPattern, 'g');
    } catch (e) {
      return res.status(400).json({ error: 'Invalid Regular Expression' });
    }
  } else {
    searchTerm = query.toLowerCase();
  }

  const workerData = {
    filesIndex,
    language,
    searchRegex,
    searchTerm,
    PREVIEW_LENGTH
  };

  try {
    const { results } = await runSearchWorker(workerData, 1000);
    res.json({ results });
  } catch (error) {
    console.error(chalk.red(error.message));
    res.status(500).json({ error: error.message });
  }
});

app.get('/view/:fileName', (req, res) => {
  const fileName = req.params.fileName;
  const fileData = filesIndex[fileName];

  if (!fileData?.visible) {
    return res.status(404).send('File not found or inaccessible.');
  }

  fs.readFile(fileData.path, 'utf-8', (err, data) => {
    if (err) {
      console.error(chalk.red(err));
      return res.status(500).send('Server Error');
    }
    res.render('view_code', { fileName, code: data });
  });
});

initializeFiles();
app.listen(PORT, () => {
  console.log(chalk.blue(`Server is running on http://localhost:${PORT}`));
});
