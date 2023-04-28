import * as crypto from "crypto";

export function randStr() {
  return crypto.randomBytes(16).toString("hex");
}

let adminPW = randStr();

export function getAdminPW() {
  return adminPW;
}
export function updateAdminPW() {
  adminPW = randStr();
}

const db = new Map<SessionT, UserDBT>();

export function getUserDB(session: string) {
  if (db.has(session)) {
    return db.get(session) as UserDBT;
  } else {
    const userDB = new Map<AuthT, gradeT>();
    userDB.set(
      {
        username: "admin",
        password: adminPW,
      },
      "admin"
    );
    db.set(session, userDB);
    return userDB;
  }
}