import { AsyncDatabase } from "promised-sqlite3";

let db: AsyncDatabase | null = null;
let init = false;
export async function getConnection() {
  if (db === null) {
    db = await AsyncDatabase.open(process.env.DB_PATH!);
  }

  if (!init) {
    await db.run(`
      CREATE TABLE IF NOT EXISTS questions (
        id TEXT PRIMARY KEY,
        uid TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT
      )
    `);

    // NOTE: Insert your uid here to receive your flag!
    await db.run(`
      CREATE TABLE IF NOT EXISTS flag_owner (
        uid TEXT PRIMARY KEY
      )
    `);
    init = true;
  }
  return db;
}

export interface Question {
  id: string;
  uid: string;
  question: string;
  answer: string;
}
