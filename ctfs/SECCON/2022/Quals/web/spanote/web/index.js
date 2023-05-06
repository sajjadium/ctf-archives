const PORT = process.env.PORT ?? "3000";

const crypto = require("node:crypto");
const fs = require("node:fs").promises;

const fastify = require("fastify")({
  logger: true,
});

fastify.register(require("@fastify/cookie"));
fastify.register(require("@fastify/session"), {
  secret: crypto.randomBytes(32).toString("base64"),
  cookie: { secure: false },
});

fastify.register(require("@fastify/formbody"));
fastify.register(require("./report"), { prefix: "/report" });

fastify.register(require("@fastify/static"), {
  root: __dirname,
  serve: false,
});

const validate = (id) => {
  if (typeof id !== "string") {
    throw Error(`Invalid id: ${id}`);
  }
  if (
    id.includes("..") ||
    id.includes("/") ||
    id.includes("\\") ||
    id.includes("%")
  ) {
    // No path traversal
    throw Error(`Invalid id: ${id}`);
  }
  return id;
};

const hash = (data) => {
  if (typeof data !== "string") {
    throw new Error("Invalid data");
  }
  return crypto.createHash("sha1").update(data).digest().toString("hex");
};

class User {
  constructor(id) {
    this.id = validate(id);
  }

  static async create() {
    const userId = crypto.randomBytes(32).toString("hex");
    await fs.mkdir(`db/${userId}`, { recursive: true });
    return new User(userId);
  }

  async createNote(content) {
    const noteId = hash(content);
    await fs.writeFile(`db/${this.id}/${noteId}`, content);
    return noteId;
  }

  async deleteNote(noteId) {
    await fs.writeFile(`db/${this.id}/${noteId}`, `deleted: ${noteId}`);
    return noteId;
  }

  sendNoteIds() {
    return fs.readdir(`db/${this.id}`);
  }

  sendNote(reply, noteId) {
    return reply.sendFile(`db/${this.id}/${noteId}`);
  }
}

fastify.get("/api/token", async (request, reply) => {
  const token = hash(request.session.userId);
  return { token };
});

fastify.get("/api/notes", async (request, reply) => {
  const user = new User(request.session.userId);
  if (request.headers["x-token"] !== hash(user.id)) {
    throw new Error("Invalid token");
  }
  return user.sendNoteIds();
});

fastify.get("/api/notes/:noteId", async (request, reply) => {
  const user = new User(request.session.userId);
  if (request.headers["x-token"] !== hash(user.id)) {
    throw new Error("Invalid token");
  }
  const noteId = validate(request.params.noteId);
  return user.sendNote(reply, noteId);
});

fastify.post("/api/notes/create", async (request, reply) => {
  const user = new User(request.session.userId);
  const content = request.body.content;
  if (typeof content !== "string") {
    throw new Error("Invalid note");
  }
  const noteId = await user.createNote(content);
  return { noteId };
});

fastify.post("/api/notes/delete", async (request, reply) => {
  const user = new User(request.session.userId);
  const noteId = validate(request.body.noteId);
  await user.deleteNote(noteId);
  return { noteId };
});

fastify.get("/", async (request, reply) => {
  const user =
    request.session.userId != null
      ? new User(request.session.userId)
      : await User.create();
  request.session.userId = user.id;

  return reply.sendFile("public/index.html");
});

fastify.get("/clear", async (request, reply) => {
  request.session.destroy();
  return reply.redirect("/");
});

fastify.listen({ port: PORT, host: "0.0.0.0" }, (err, _address) => {
  if (err) {
    fastify.log.error(err);
    process.exit(1);
  }
});
