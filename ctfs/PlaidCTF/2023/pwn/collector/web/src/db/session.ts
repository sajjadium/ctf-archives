import { redirect } from "solid-start/server";
import { createCookieSessionStorage } from "solid-start/session";
import sql from ".";
import bcrypt from 'bcryptjs';
import { insert } from "solid-js/web";

// stupid hack to get around bcryptjs issues
(global as any)['se' + 'lf'] = global;

type LoginForm = {
  username: string;
  plaintextPassword: string;
};

type User = {
  id: string,
  username: string,
  password: string,
};

const saltRounds = 10;

export async function register(username: string, plaintextPassword: string): Promise<User> {
  const password = await bcrypt.hash(plaintextPassword, saltRounds);
  return await sql.begin(async sql => {
    const insertedResult = await sql`
      INSERT INTO users (username, password)
      VALUES (${username}, ${password})
      RETURNING id;
    `;
    if (insertedResult.length !== 1) {
      throw 'BUG: Wrong number of results from inserting user';
    }
    const id = String(insertedResult[0].id);
    await sql`
      INSERT INTO inventory (user_id, item_id, count)
      SELECT ${id}, item_id, count FROM initial_inventory
    `
    return { id, username, password };
  });
}

export async function findUserByName(username: string): Promise<User | undefined> {
  try {
    const results = await sql`
      SELECT id, password FROM users WHERE username = ${username}
    `;
    if (results.length !== 1) return;
    const { id, password } = results[0];
    return { id, username, password };
  } catch (e) {
    console.error('BUG: unable to find user', e);
    return;
  }
}

export async function findUser(id: string): Promise<User | undefined> {
  try {
    const results = await sql`
      SELECT username, password FROM users WHERE id = ${id}
    `;
    if (results.length !== 1) return;
    const { username, password } = results[0];
    return { id, username, password };
  } catch (e) {
    console.error('BUG: unable to find user', e);
    return;
  }
}

export async function login(user: User, plaintextPassword: string): Promise<User | undefined> {
  if (await bcrypt.compare(plaintextPassword, user.password)) {
    return user;
  }
}

const storage = createCookieSessionStorage({
  cookie: {
    name: "collector",
    secure: false,
    secrets: [process.env.JWT_SECRET ?? "jwt-secret"],
    sameSite: "lax",
    path: "/",
    maxAge: 60 * 60 * 24 * 30,
    httpOnly: true,
  },
});

export function getUserSession(request: Request) {
  return storage.getSession(request.headers.get("Cookie"));
}

export async function getUserId(request: Request) {
  const session = await getUserSession(request);
  const userId = session.get("userId");
  if (!userId || typeof userId !== "string") return null;
  return userId;
}

export async function requireUserId(
  request: Request,
  redirectTo: string = new URL(request.url).pathname
) {
  const session = await getUserSession(request);
  const userId = session.get("userId");
  if (!userId || typeof userId !== "string") {
    const searchParams = new URLSearchParams([["redirectTo", redirectTo]]);
    throw redirect(`/login?${searchParams}`);
  }
  return userId;
}

export async function getUser(request: Request) {
  const userId = await getUserId(request);
  if (typeof userId !== "string") {
    return null;
  }

  try {
    const user = await findUser(userId);
    return user;
  } catch {
    throw await logout(request);
  }
}

export async function logout(request: Request) {
  const session = await storage.getSession(request.headers.get("Cookie"));
  return redirect("/login", {
    headers: {
      "Set-Cookie": await storage.destroySession(session),
    },
  });
}

export async function createUserSession(userId: string, redirectTo: string) {
  const session = await storage.getSession();
  session.set("userId", userId);
  return redirect(redirectTo, {
    headers: {
      "Set-Cookie": await storage.commitSession(session),
    },
  });
}
