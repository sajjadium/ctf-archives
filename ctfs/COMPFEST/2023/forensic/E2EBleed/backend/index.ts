import { WebSocketServer, WebSocket, RawData } from "ws";
import storage from "node-persist";
import bcrypt from "bcrypt";
import express from "express";
import expressWs from "express-ws";
import crypto from "crypto";
import cors from "cors";

const saltRounds = 10;

interface TargetedMsg {
  fromUsername: string;
  targetUsername: string;
}

interface IdentMsg {
  username: string;
  password: string;
}

type Message =
  | {
      type: "ident";
      data: IdentMsg;
    }
  | {
      type: "message" | "ack" | "init";
      data: TargetedMsg;
    };

interface ResponseMsg {
  type: "server";
  action: "auth" | "message";
  message: string;
}

async function setupStorage() {
  await storage.init({
    dir: "persist",
  });
}

class ConnectionManager {
  connToUsername = new Map<WebSocket, string>();
  usernameToConn = new Map<string, WebSocket>();

  getFromConn(conn: WebSocket) {
    return this.connToUsername.get(conn);
  }

  getFromUsername(username: string) {
    return this.usernameToConn.get(username);
  }

  set(conn: WebSocket, username: string) {
    this.connToUsername.set(conn, username);
    this.usernameToConn.set(username, conn);
  }

  delete(ident: WebSocket | string) {
    if (typeof ident == "string") {
      const conn = this.usernameToConn.get(ident);
      this.usernameToConn.delete(ident);
      conn && this.connToUsername.delete(conn);
    } else {
      const username = this.connToUsername.get(ident);
      this.connToUsername.delete(ident);
      username && this.usernameToConn.delete(username);
    }
  }
}

const connections = new ConnectionManager();

async function identMessage(
  conn: WebSocket,
  message: Message
): Promise<ResponseMsg> {
  if (message.type != "ident")
    return { type: "server", action: "auth", message: "" };

  let currentIdent = connections.getFromConn(conn);
  if (currentIdent !== undefined) {
    return {
      type: "server",
      action: "auth",
      message: "You are identified already!",
    };
  }

  let { username, password } = message.data;
  username = username.trim();
  password = password.trim();
  if (username == "" || password == "") {
    return {
      type: "server",
      action: "auth",
      message: "Invalid auth!",
    };
  }

  const expectedPassword = await storage.getItem(username);
  if (expectedPassword !== undefined) {
    // Log in
    const result = await bcrypt.compare(password, expectedPassword);
    if (!result) {
      return { type: "server", action: "auth", message: "Invalid password!" };
    }

    connections.set(conn, username);
    return { type: "server", action: "auth", message: "Authenticated" };
  }

  // Register
  const hashedPass = await bcrypt.hash(password, saltRounds);
  await storage.setItem(username, hashedPass);
  connections.set(conn, username);
  return { type: "server", action: "auth", message: "Authenticated" };
}

async function onWebsocketMessage(conn: WebSocket, data: RawData) {
  const message: Message = JSON.parse(data.toString());
  if (message.type == "ident") {
    conn.send(JSON.stringify(await identMessage(conn, message)));
  } else {
    const targetMsg = message.data as TargetedMsg;
    const targetConn = connections.getFromUsername(targetMsg.targetUsername);
    if (!targetConn) {
      conn.send(
        JSON.stringify({
          type: "server",
          action: "message",
          message: "Target not online",
        })
      );
      return;
    }

    targetConn.send(JSON.stringify(message));
    conn.send(
      JSON.stringify({ type: "server", action: "message", message: "Sent" })
    );
  }
}

var appExpress = express();
var { app } = expressWs(appExpress);
app.use(cors());

app.ws("/", function (ws) {
  ws.on("error", console.error);
  ws.on("message", (data) => onWebsocketMessage(ws, data));
  ws.on("close", () => connections.delete(ws));
});

app.get("/prime/:bits", function (req, res) {
  if (Number(req.params.bits) > 2048 || Number(req.params.bits) < 2) {
    return res.send("no");
  }

  crypto.generatePrime(
    Number(req.params.bits),
    { bigint: true },
    (err, prime) => {
      res.send(prime.toString());
    }
  );
});

setupStorage();
app.listen(8080);
