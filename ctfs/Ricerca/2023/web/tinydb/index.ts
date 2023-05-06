import fastify from "fastify";
import { fastifySession } from "@fastify/session";
import fastifyCookie from "@fastify/cookie";
import * as fs from "fs";
import { getUserDB, randStr, getAdminPW, updateAdminPW } from "./db";
import flag from "./flag";

const server = fastify();
server.register(fastifyCookie);
server.register(fastifySession, {
  secret: randStr(),
  cookie: { secure: false },
});

server.get("/", async (_, response) => {
  const html = await fs.promises.readFile("./src/index.html", "utf-8");
  response.type("text/html").send(html);
});

server.get("/admin", async (_, response) => {
  const html = await fs.promises.readFile("./src/admin.html", "utf-8");
  response.type("text/html").send(html);
});

type UserBodyT = Partial<AuthT>;
server.post<{ Body: UserBodyT }>("/set_user", async (request, response) => {
  const { username, password } = request.body;
  const session = request.session.sessionId;
  const userDB = getUserDB(session);

  let auth = {
    username: username ?? "admin",
    password: password ?? randStr(),
  };
  if (!userDB.has(auth)) {
    userDB.set(auth, "guest");
  }

  if (userDB.size > 10) {
    // Too many users, clear the database
    userDB.clear();
    auth.username = "admin";
    auth.password = getAdminPW();
    userDB.set(auth, "admin");
    auth.password = "*".repeat(auth.password.length);
  }

  const rollback = () => {
    const grade = userDB.get(auth);
    updateAdminPW();
    const newAdminAuth = {
      username: "admin",
      password: getAdminPW(),
    };
    userDB.delete(auth);
    userDB.set(newAdminAuth, grade ?? "guest");
  };
  setTimeout(() => {
    // Admin password will be changed due to hacking detected :(
    if (auth.username === "admin" && auth.password !== getAdminPW()) {
      rollback();
    }
  }, 2000 + 3000 * Math.random()); // no timing attack!

  const res = {
    authId: auth.username,
    authPW: auth.password,
    grade: userDB.get(auth),
  };

  response.type("application/json").send(res);
});

server.post<{ Body: AuthT }>("/get_flag", async (request, response) => {
  const { username, password } = request.body;
  const session = request.session.sessionId;
  const userDB = getUserDB(session);
  for (const [auth, grade] of userDB.entries()) {
    if (
      auth.username === username &&
      auth.password === password &&
      grade === "admin"
    ) {
      response
        .type("application/json")
        .send({ flag: `great! here is your flag: ${flag}` });
      return;
    }
  }
  response.type("application/json").send({ flag: "no flag for you :)" });
});

server.listen({ host: "0.0.0.0", port: 8888 }, (_, address) => {
  console.log(`Server listening at ${address}`);
});
