import * as bl from "beautiful-log";
import { spawn } from "child_process";
import * as path from "path";
import { Server } from "socket.io";

import { transaction } from "./db";
import { JobRequest, SocketState, SocketWithState } from "./types";

const LAUNCH_DELAY = 2000;
const TIMEOUT = 15000;

const log = bl.make("workers");

export function startWorkers(count: number, io: Server) {
  for (let i = 0; i < count; i++) {
    worker(i, io);
  }
}

function sleep(time: number) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

async function worker(index: number, io: Server) {
  while (true) {
    try {
      const jobCompleted = await transaction(async (client) => {
        const jobResult = await client.query<{
          uid: string;
          job: JobRequest;
          socket_id: string;
        }>(
          "SELECT * FROM job WHERE completed_at IS NULL ORDER BY created_at LIMIT 1 FOR UPDATE SKIP LOCKED"
        );

        if (jobResult.rowCount !== 1) {
          return false;
        }

        const { uid, job, socket_id: socketId } = jobResult.rows[0];

        const socket = io.sockets.sockets.get(socketId) as SocketWithState;

        if (!socket) {
          log(
            `[worker ${index}] Skipping job because socket is no longer connected.`
          );
        } else {
          await doJob(index, job, socket);
        }

        await client.query(
          "UPDATE job SET completed_at = NOW() WHERE uid = $1",
          [uid]
        );
        return true;
      });

      if (!jobCompleted) {
        log(
          `[worker ${index}] No job found; sleeping for 1s and trying again.`
        );
        await sleep(1000);
      } else {
        log(`[worker ${index}] Job completed!  Looking for a new job.`);
      }
    } catch (err) {
      log.error(err);
    }
  }
}

function spawnPromise(
  command: string,
  args: string[],
  options: Parameters<typeof spawn>[2]
): Promise<void> {
  return new Promise((resolve, reject) => {
    const proc = spawn(command, args, options);
    proc.on("exit", (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(`spawn exited with non-zero exit code: ${code}`);
      }
    });
  });
}

async function doJob(
  index: number,
  job: JobRequest,
  socket: SocketWithState
) {
  log(`[worker ${index}] Launching instance for URL <cyan>${job.url}</cyan>.`);

  const cwd = path.join(__dirname, "../../../instance");

  const env = {
    ATTACKER_URL: job.url,
    FLAG: process.env.FLAG,
  };

  socket.state = {
    kind: SocketState.Kind.Accepted,
    request: job,
    launchingAt: Date.now() + LAUNCH_DELAY,
  };
  socket.emit("accepted", {
    launchingAt: socket.state.launchingAt,
  });

  await sleep(LAUNCH_DELAY);

  await spawnPromise(
    "/usr/local/bin/docker-compose",
    ["-p", `puppet_instance_${index}`, "up", "-d", "--no-build"], // You MUST build the containers on the host before starting
    {
      cwd,
      stdio: ["ignore", process.stdout, process.stderr],
      env,
    }
  );

  socket.state = {
    kind: SocketState.Kind.Processing,
    request: job,
    until: Date.now() + TIMEOUT,
  };
  socket.emit("processing", {
    until: socket.state.until,
  });

  log(`[worker ${index}] Instance is up, waiting for ${TIMEOUT}ms.`);
  const reason = await Promise.race([
    sleep(TIMEOUT).then(() => "timeout exceeded"),
    new Promise((resolve) =>
      socket.once("disconnect", () => resolve("socket disconnected"))
    ),
  ]);

  try {
    log(`[worker ${index}] Killing the instance (${reason}).`);
    await spawnPromise(
      "/usr/local/bin/docker-compose",
      ["-p", `puppet_instance_${index}`, "down", "-t", "0"],
      {
        cwd,
        stdio: ["ignore", process.stdout, process.stderr],
        env,
      }
    );
    socket.state = { kind: SocketState.Kind.Waiting };
    socket.emit("done");
  } catch (err) {
    // Guess it was already dead /shrug
  }
}
