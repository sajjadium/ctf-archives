const express = require("express");
const http = require("http");
const socketio = require("socket.io");
const sqlite3 = require("sqlite3");
const crypto = require("crypto");
const path = require("path");

const BIND_ADDR = process.env.BIND_ADDR || "0.0.0.0";
const PORT = process.env.PORT || "1024";

const app = express();
app.use(express.json());
const server = http.createServer(app);
const io = socketio(server);
const db = new sqlite3.Database("db.db");

const sendResponse = (res, status, data) => {
  res.status(status);
  res.json(data);
  res.end();
};

app.post("/register", (req, res) => {
  let username = req.body["username"] || "";
  let password = req.body["password"] || "";

  if (
    typeof username !== "string" ||
    typeof password !== "string" ||
    username.length === 0 ||
    password.length === 0 ||
    username.length > 50
  )
    return sendResponse(res, 400, { error: "Invalid request" });

  db.get("SELECT * FROM users WHERE username = ?", username, (err, row) => {
    if (err) return sendResponse(res, 500, { error: "Failed to create user" });

    if (row) return sendResponse(res, 400, { error: "User already exists" });

    let passHash = crypto.createHash("sha256").update(password).digest("hex");
    let token = crypto.randomBytes(16).toString("hex");
    db.run(
      "INSERT INTO users(username, password, token) VALUES(?, ?, ?)",
      username,
      passHash,
      token,
      (err) => {
        if (err)
          return sendResponse(res, 500, { error: "Failed to create user" });

        return sendResponse(res, 200, { token: token });
      }
    );
  });
});

app.post("/login", (req, res) => {
  let username = req.body["username"] || "";
  let password = req.body["password"] || "";

  if (
    typeof username !== "string" ||
    typeof password !== "string" ||
    username.length === 0 ||
    password.length === 0 ||
    username.length > 50
  )
    return sendResponse(res, 400, { error: "Invalid request" });

  let passHash = crypto.createHash("sha256").update(password).digest("hex");
  db.get(
    "SELECT token from users WHERE username = ? AND password = ?",
    username,
    passHash,
    (err, row) => {
      if (err)
        return sendResponse(res, 500, { error: "Failed to fetch token" });
      if (!row) return sendResponse(res, 401, { error: "Invalid credentials" });

      return sendResponse(res, 200, { token: row["token"] });
    }
  );
});

app.get("/message", (req, res) => {
  let id = req.query.id?.toString() || "";
  let token = req.query.token?.toString() || "";
  let cb = req.query.cb?.toString() || "";

  cb = cb.replace(/[^a-zA-Z0-9\.\[\]]/g, "");

  db.get("SELECT username FROM users WHERE token = ?", token, (err, row) => {
    if (err)
      return sendResponse(res, 500, { message: "Internal server error" });

    if (!row) return sendResponse(res, 400, { message: "Invalid token" });

    let username = row["username"];
    db.get(
      "SELECT sender, message, time FROM messages WHERE (recipient = ? OR sender = ?) AND id = ?",
      username,
      username,
      id,
      (err, row) => {
        if (err)
          return sendResponse(res, 500, { message: "Internal server error" });

        if (!row)
          return sendResponse(res, 404, { message: "Message not found" });

        res.set("Content-Type", "application/javascript");
        res.send(
          `${cb}(${JSON.stringify({
            time: row["time"],
            sender: row["sender"],
            message: row["message"],
          })})`
        );
        res.end();
      }
    );
  });
});

app.get("/print", (req, res) => {
  res.sendFile(path.join(__dirname, "print.html"));
});

// middleware to validate the user token
io.use((socket, next) => {
  const token = socket.handshake.auth.token;

  db.get("SELECT username FROM users WHERE token = ?", token, (err, row) => {
    if (err) return next(new Error("Internal server error"));

    if (!row) return next(new Error("Invalid token"));

    socket.username = row["username"];
    next();
  });
});

io.on("connection", (socket) => {
  socket.join(socket.username);

  // data structure: { message: "some message", recipient: "username" }
  // stores a message in the database and notifies the recipient
  socket.on("sendMessage", (data) => {
    if (typeof data !== "object") return;

    let message = data["message"] || "";
    let recipient = data["recipient"] || "";
    let time = new Date().toISOString();

    if (message.length > 250) message = message.substring(0, 250);

    if (!message || !recipient) return;

    db.run(
      "INSERT INTO messages(sender, recipient, message, time) VALUES(?, ?, ?, ?)",
      socket.username,
      recipient,
      message,
      time,
      function (err) {
        if (err) return;

        let newMsg = {
          id: this.lastID,
          sender: socket.username,
          recipient: recipient,
          message: message,
          time: time,
        };

        io.to(recipient).emit("newMessage", newMsg);
        if (recipient !== socket.username)
          io.to(socket.username).emit("newMessage", newMsg);
      }
    );
  });

  // data structure: { user: "username" }
  // sends all recent messages with a specific user to the client
  socket.on("getMessages", (data) => {
    if (typeof data !== "object") return;

    let user = data["user"] || "";

    if (!user) return;

    // support gets all messages regardless of the sender
    if (socket.username === "support") {
      db.all(
        "SELECT id, sender, recipient, message, time FROM messages WHERE recipient='support'",
        (err, rows) => {
          if (err) return;

          socket.emit("getMessages", { messages: rows || [] });
        }
      );

      return;
    }

    db.all(
      "SELECT id, sender, recipient, message, time FROM messages WHERE (sender=? AND recipient=?) OR (sender=? AND recipient=?)",
      socket.username,
      user,
      user,
      socket.username,
      (err, rows) => {
        if (err) return;

        socket.emit("getMessages", { messages: rows || [] });
      }
    );
  });

  // send all usernames that the client user interacted with to the client
  socket.on("contacts", () => {
    db.all(
      "SELECT sender, recipient FROM messages WHERE sender=? OR recipient=?",
      socket.username,
      socket.username,
      (err, rows) => {
        if (err) return;

        const contacts = [];
        rows.forEach((row) => {
          if (row["sender"] === socket.username)
            contacts.push(row["recipient"]);
          else contacts.push(row["sender"]);
        });

        socket.emit("contacts", { contacts: [...new Set(contacts)] });
      }
    );
  });
});

// initialize database
db.exec(
  `
  CREATE TABLE IF NOT EXISTS "users"(
    "id" INTEGER PRIMARY KEY NOT NULL,
    "username" VARCHAR(50) NOT NULL,
    "password" VARCHAR(64) NOT NULL,
    "token" VARCHAR(32) NOT NULL
  );

  CREATE TABLE IF NOT EXISTS "messages"(
    "id" INTEGER PRIMARY KEY NOT NULL,
    "sender" VARCHAR(50) NOT NULL,
    "recipient" VARCHAR(50) NOT NULL,
    "message" VARCHAR(500),
    "time" DATETIME DEFAULT CURRENT_TIMESTAMP
  );
`,
  (err) => {
    if (err) {
      console.log(err);
      process.exit(1);
    }

    server.listen(PORT, BIND_ADDR, () => {
      console.log(`Running on ${BIND_ADDR}:${PORT}...`);
    });
  }
);
