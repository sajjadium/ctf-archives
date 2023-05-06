import { createHash, randomBytes } from "crypto";

import { pool, transaction } from "./db";
import { JobRequest } from "./types";

export interface Challenge {
  uid: string;
  prefix: string;
  difficulty: number;
}

async function getCurrentDifficulty() {
  const result = await pool.query(
    "SELECT COUNT(*) FROM job WHERE completed_at IS NULL"
  );
  const { count } = result.rows[0];
  return Math.min(32, 16 + Math.floor(Math.log(count + 1)));
}

export async function generateChallenge(): Promise<Challenge> {
  const prefix = randomBytes(12).toString("hex");
  const difficulty = await getCurrentDifficulty();
  const result = await pool.query(
    "INSERT INTO challenge (prefix, difficulty, deadline) VALUES ($1, $2, NOW() + interval '5 minutes') RETURNING *",
    [prefix, difficulty]
  );
  const { uid } = result.rows[0];
  return { uid, prefix, difficulty };
}

export async function validateChallenge(
  uid: string,
  response: string,
  job: JobRequest,
  socketId: string
): Promise<string | undefined> {
  return await transaction(async (client) => {
    const result = await client.query(
      "SELECT * FROM challenge WHERE uid = $1 AND deadline > NOW() FOR UPDATE LIMIT 1",
      [uid]
    );

    if (result.rowCount !== 1) {
      throw new Error("Invalid challenge");
    }

    const task: { uid: string; prefix: string; difficulty: number } =
      result.rows[0];
    const resultBuffer = createHash("sha256")
      .update(task.prefix)
      .update(response)
      .digest();
    let value = resultBuffer.readUInt32BE(0);
    value >>>= 32 - task.difficulty;

    await client.query("DELETE FROM challenge WHERE uid = $1", [uid]);

    if (value !== 0) {
      return;
    }

    const jobResult = await client.query<{ uid: string }>(
      "INSERT INTO job (job, socket_id) VALUES ($1, $2) RETURNING uid",
      [job, socketId]
    );
    return jobResult.rows[0].uid;
  });
}
