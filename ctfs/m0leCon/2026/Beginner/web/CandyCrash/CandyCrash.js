const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const crypto = require("crypto");

const engine = require("./client/engine.js");

const app = express();
app.use(express.json({ limit: "1mb" }));
app.use(cors());

const PORT = Number(process.env.PORT || 3000);
const TARGET_SCORE = Number(process.env.TARGET_SCORE || 10000);
const SESSION_TTL_MS = Number(process.env.SESSION_TTL_MS || 1000 * 60 * 30);
const MAX_MOVES = Number(process.env.MAX_MOVES || 600);

let FLAG = "ptm{placeholder_flag}";
try {
  FLAG = fs.readFileSync("/app/FLAG", "utf8").trim();
} catch (err) {
  console.error("[-] Warning: Could not read flag file, using placeholder");
}

const sessions = new Map();
const replayDir = path.join(__dirname, "replays");
fs.mkdirSync(replayDir, { recursive: true });

const replayMetadata = new Map();
const REPLAY_TTL_MS = 10 * 60 * 1000; // 10 minuti

function cleanReplayDirectory() {
  try {
    const files = fs.readdirSync(replayDir);
    for (const file of files) {
      if (file.endsWith('.json')) {
        fs.unlinkSync(path.join(replayDir, file));
      }
    }
    console.log(`[+] Cleaned ${files.length} replay files on startup`);
  } catch (err) {
    console.error('[-] Error cleaning replay directory:', err.message);
  }
}

cleanReplayDirectory();

function createSession() {
  const sessionId = crypto.randomUUID();
  const seed = crypto.randomInt(1, 0x7ffffffe);
  const createdAt = Date.now();
  sessions.set(sessionId, { seed, createdAt, submissions: [] });
  return { sessionId, seed };
}

function purgeSessions() {
  const now = Date.now();
  for (const [id, session] of sessions.entries()) {
    if (now - session.createdAt > SESSION_TTL_MS) {
      sessions.delete(id);
    }
  }
}
setInterval(purgeSessions, 5 * 60 * 1000).unref();

function purgeReplays() {
  const now = Date.now();
  for (const [sessionId, metadata] of replayMetadata.entries()) {
    if (now - metadata.createdAt > REPLAY_TTL_MS) {
      const filePath = path.join(replayDir, `${sessionId}.json`);
      fs.unlink(filePath, (err) => {
        if (!err) {
          replayMetadata.delete(sessionId);
        }
      });
    }
  }
}
setInterval(purgeReplays, 60 * 1000).unref();

function replaySession(seed, submittedMoves) {
  const rng = engine.createRng(seed);
  const board = engine.generateBoard(rng);
  const moves = Array.isArray(submittedMoves)
    ? submittedMoves.slice(0, MAX_MOVES)
    : [];

  const timeline = [];
  let score = 0;

  for (let idx = 0; idx < moves.length; idx++) {
    const move = moves[idx] || {};
    const from = Number(move.from);
    const to = Number(move.to);
    if (!Number.isInteger(from) || !Number.isInteger(to)) {
      continue;
    }

    const result = engine.attemptMove(board, from, to, rng);
    if (!result.valid) {
      timeline.push({ idx, from, to, accepted: false, delta: 0 });
      continue;
    }
    score += result.score;
    timeline.push({ idx, from, to, accepted: true, delta: result.score });
  }

  return { score, timeline };
}

function persistReplay(sessionId, seed, timeline, moves) {
  const payload = {
    sessionId,
    seed,
    createdAt: new Date().toISOString(),
    timeline,
    moves,
  };
  const filePath = path.join(replayDir, `${sessionId}.json`);
  replayMetadata.set(sessionId, { createdAt: Date.now() });
  fs.promises.writeFile(filePath, JSON.stringify(payload, null, 2)).catch(() => {
    /* ignore */
  });
}

app.get("/api/health", (req, res) => {
  res.json({
    status: "ok",
    sessions: sessions.size,
    targetScore: TARGET_SCORE,
  });
});

app.post("/api/session", (req, res) => {
  const { sessionId, seed } = createSession();
  res.json({ sessionId, seed, targetScore: TARGET_SCORE });
});

app.post("/api/submit", (req, res) => {
  const { sessionId, moves } = req.body || {};
  if (!sessionId) {
    return res.status(400).json({ error: "Missing sessionId" });
  }
  const session = sessions.get(sessionId);
  if (!session) {
    return res.status(404).json({ error: "Unknown session" });
  }

  const { score, timeline } = replaySession(session.seed, moves);
  session.submissions.push({ at: Date.now(), score });
  persistReplay(sessionId, session.seed, timeline, moves);

  if (score >= TARGET_SCORE) {
    return res.json({
      score,
      verified: true,
      flag: FLAG,
      timeline,
    });
  }

  res.json({
    score,
    verified: false,
    remaining: Math.max(TARGET_SCORE - score, 0),
    timeline,
  });
});

app.get("/api/replays", (req, res) => {
  const fileParam = typeof req.query.file === "string" ? req.query.file : "";
  if (!fileParam) {
    const entries = fs.readdirSync(replayDir).map((name) => ({ name }));
    return res.json({ files: entries });
  }

  const sanitized = fileParam.replace(/\.\./g, "");
  const target = path.join(replayDir, sanitized);
  fs.readFile(target, "utf8", (err, data) => {
    if (err) {
      return res.status(404).json({ error: "Replay not found" });
    }
    res.type("application/json").send(data);
  });
});

app.post("/api/debug/run", (req, res) => {
  const script = (req.body && req.body.script ? String(req.body.script) : "").trim();
  if (!script) {
    return res.status(400).json({ error: "Empty script" });
  }
  if (script.length > 2000) {
    return res.status(400).json({ error: "Script too long" });
  }
  if (/process|require|global/i.test(script)) {
    return res.status(400).json({ error: "Blocked tokens" });
  }

  const sessionId = req.body && req.body.sessionId;
  const session = sessions.get(sessionId) || null;
  if (sessionId && !session) {
    return res.status(404).json({ error: "Unknown session" });
  }
  const sandboxRng = engine.createRng(session ? session.seed : 1337);
  const output = [];

  const sandbox = {
    console: {
      log: (...args) => output.push(args.map((a) => String(a)).join(" ")),
    },
    timeline: session ? session.submissions : [],
    getNextRandom: () => sandboxRng(),
    setResult(value) {
      sandbox.result = value;
    },
    Buffer,
  };

  Object.defineProperty(sandbox, "__internalFlag", {
    value: FLAG,
    enumerable: false,
    writable: false,
  });

  sandbox.inspectReplay = function inspectReplay(file) {
    const trimmed = typeof file === "string" ? file.replace(/\.\./g, "") : "";
    const filePath = path.join(replayDir, trimmed);
    return fs.readFileSync(filePath, "utf8");
  };

  vm.createContext(sandbox);

  try {
    const result = vm.runInContext(script, sandbox, { timeout: 250 });
    res.json({
      result: sandbox.result ?? result ?? null,
      logs: output,
    });
  } catch (error) {
    res.status(400).json({ error: error.message, logs: output });
  }
});

app.use((req, res) => {
  res.status(404).json({ error: "Not found" });
});

app.listen(PORT, () => {
  console.log(`[+] Candy Crash backend listening on port ${PORT}`);
});
