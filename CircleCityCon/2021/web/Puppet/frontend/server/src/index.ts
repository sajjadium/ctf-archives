import * as bl from "beautiful-log";
import express from "express";
import { Server } from "http";
import nconf from "nconf";
import { M, marshal, Marshaller } from "@zensors/sheriff";
import { JobRequest, SocketState, SocketWithState } from "./types";
import { generateChallenge, validateChallenge } from "./challenge";

import { Server as SocketIoServer } from "socket.io";

import { pool } from "./db";
import { startWorkers } from "./workers";

nconf.argv().env();
const PORT = nconf.get("PORT") ?? 8080;
const MAX_WORKERS = parseInt(nconf.get("MAX_WORKERS") ?? "4", 10);

bl.init("frontend", "console");
const log = bl.make("top");

const app = express();

const httpServer = new Server(app);
const io = new SocketIoServer(httpServer);

function defineSocketHandler<K extends SocketState.Kind, T>(
  socket: SocketWithState,
  name: string,
  kind: K,
  marshaller: Marshaller<T>,
  fn: (
    socket: SocketWithState,
    state: SocketState & { kind: K },
    arg: T
  ) => Promise<void>
) {
  socket.on(name, async (arg: unknown) => {
    if (socket.state.kind !== kind) {
      socket.emit("error", "invalid socket state");
      socket.disconnect();
      return;
    }

    try {
      marshal(arg, marshaller);
      await fn(socket, socket.state as SocketState & { kind: K }, arg);
    } catch (err) {
      log.error(err);
      socket.emit("error", "something went wrong");
      socket.disconnect();
    }
  });
}

io.on("connection", (socket: SocketWithState) => {
  socket.state = { kind: SocketState.Kind.Waiting };

  defineSocketHandler(
    socket,
    "submitJob",
    SocketState.Kind.Waiting,
    JobRequest.Marshaller,
    async (socket, _state, request) => {
      const challenge = await generateChallenge();
      socket.state = { kind: SocketState.Kind.Challenge, request, challenge };
      socket.emit("challenge", challenge);
    }
  );

  defineSocketHandler(
    socket,
    "submitChallenge",
    SocketState.Kind.Challenge,
    M.str,
    async (socket, state, response) => {
      const uid = await validateChallenge(
        state.challenge.uid,
        response,
        state.request,
        socket.id
      );

      if (uid === undefined) {
        throw new Error("invalid challenge response");
      }

      socket.state = {
        kind: SocketState.Kind.Queued,
        request: state.request,
        jobUid: uid,
      };
      socket.emit("queued");

      const updatePosition = async () => {
        if (socket.state.kind !== SocketState.Kind.Queued) {
          return;
        }

        const result = await pool.query<{ count: number }>(
          `
SELECT COUNT(*)
FROM job
WHERE completed_at IS NULL AND created_at < (SELECT created_at FROM job WHERE uid = $1)
`,
          [socket.state.jobUid]
        );

        socket.emit("position", result.rows[0].count);
        setTimeout(updatePosition, 5000);
      };

      updatePosition();
    }
  );
});

app.use(express.static("public"));

httpServer.listen(PORT, () => {
  console.log(`Listening on ${PORT}`);
  startWorkers(MAX_WORKERS, io);
});
