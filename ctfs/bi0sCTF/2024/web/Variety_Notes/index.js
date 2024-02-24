const express = require("express");
const bodyParser = require("body-parser");
const session = require("express-session");
const crypto = require("crypto");
const fs = require("fs");
const filehound = require("filehound");
const sanitize = require("sanitize-filename");
const { visit } = require("./bot");
const {
  createUser,
  getUser,
  createNote,
  getNote,
  deleteNote,
  shareNote,
  getsharedNote,
} = require("./db");

const app = express();
const port = 3000;
const authUser = process.env.INSTANCE_USERNAME || 'admin'
const authpass = process.env.INSTANCE_PASSWORD || 'password'

const adminPass = crypto.randomBytes(16).toString("hex");
const adminUUID = createUser("admin", adminPass);

console.log(
  `Admin Initialised with UUID: ${adminUUID} and Password: ${adminPass}`
);

createNote(
  "Flag",
  process.env.FLAG || "bi0sctf{this_is_a_fake_flag}",
  adminUUID
);
console.log(`username ${authUser} password ${authpass}`);
function authentication(req, res, next) {
  const authHeader = req.headers.authorization;

  console.log(authHeader);

  if (!authHeader) {
    console.log("no header")
    const err = new Error('You are not authenticated!');
    res.setHeader('WWW-Authenticate', 'Basic');
    err.status = 401;
    return next(err);
  }

  const [, base64Credentials] = authHeader.split(' ');
  const credentials = Buffer.from(base64Credentials, 'base64').toString('ascii');
  const [username, password] = credentials.split(':');
console.log(username,password)
  if (username === authUser && password === authpass) {
    console.log("sucess")
    // If Authorized user
    next();
  } else {
    const err = new Error('You are not authenticated!');
    res.setHeader('WWW-Authenticate', 'Basic');
    err.status = 401;
    return next(err);
  }
}
app.use(authentication)

const appURL =
	  process.env.INSTANCE_IP && process.env.INSTANCE_PORT
    ? process.env.INSTANCE_IP + process.env.INSTANCE_PORT + "/"
    : "http://localhost:3000/";

app.use(
  session({
    secret: crypto.randomBytes(16).toString("hex"),
    resave: true,
    saveUninitialized: true,
  })
);

app.use((req, res, next) => {
  res.setHeader(
    "Content-Security-Policy",
    `
    default-src ${
      req.session && req.session.user
        ? appURL + req.session.user + "/"
        : "'none'"
    };
    script-src 'unsafe-inline' 'self';
    object-src 'none';
    base-uri 'none';
    connect-src 'none' ;
    navigate-to 'self';
    `
      .trim()
      .replace(/\s+/g, " ")
  );

  res.setHeader("Cache-Control", "no-cache,no-store");
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "SAMEORIGIN");
  res.setHeader("Referrer-Policy", "no-referrer");
  res.setHeader("Cross-Origin-Embedder-Policy", "require-corp");
  res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
  res.setHeader("Cross-Origin-Resource-Policy", "same-origin");
  res.setHeader("Document-Policy", "force-load-at-top");
  //TODO: Add more headers
  next();
});

app.use(express.static("./public"));
app.set("view engine", "ejs");

app.use(bodyParser.urlencoded({ extended: false }));

const loggedin = (req, res, next) => {
  if (req.session && req.session.user) {
    next();
  } else {
    res.redirect("/login");
  }
};

function checkSecFetchDest(req, res, next) {
  const secFetchDest = req.header("sec-fetch-dest");

  const blacklist = [
    "image",
    "script",
    "serviceworker",
    "sharedworker",
    "style",
    "video",
    "worker",
    "empty",
  ];

  if (secFetchDest && blacklist.includes(secFetchDest.toLowerCase())) {
    res.status(400).send("Invalid request");
  } else {
    next();
  }
}

const checkStr = (str) => {
  return str && typeof str === "string" && str.length > 0;
};

const checkTitle = (title) => {
  return checkStr(title) && /^[a-zA-Z0-9-\s]+$/.test(title);
};

app.use(checkSecFetchDest);
app.get("/register", (req, res) => {
  if (req.session && req.session.user) {
    return res.redirect(`/${req.session.user}`);
  }
  return res.render("register");
});

app.post("/register", (req, res) => {
  try {
    const { username, password } = req.body;

    if (!checkStr(username) || !checkStr(password)) {
      return res.send("Invalid username or password.");
    }

    const userId = createUser(username, password);

    if (!userId) {
      return res.send("Username already exists.");
    }

    req.session.user = userId;

    return res.redirect("/");
  } catch (err) {
    return res.send("Error");
  }
});

app.get("/login", (req, res) => {
  return res.render("login");
});

app.post("/login", (req, res) => {
  try {
    const { username, password } = req.body;

    if (!checkStr(username) || !checkStr(password)) {
      return res.send("Invalid username or password.");
    }

    const user = getUser(username, password);

    if (user) {
      req.session.user = user.id;
      return res.redirect(`/${user.id}`);
    }
    return res.send("Invalid username or password.");
  } catch (err) {
    return res.send("Error");
  }
});

app.get("/", loggedin, (req, res) => {
  const uuid = req.session.user;
  return res.redirect(`/${uuid}`);
});

app.post("/create", loggedin, (req, res) => {
  try {
    const { title, note } = req.body;

    if (!checkStr(title) || !checkStr(note) || !checkTitle(title)) {
      return res.send("Invalid title or note.");
    }
    const noteid = createNote(title, note, req.session.user);

    return res.redirect(`/${req.session.user}/${noteid}`);
  } catch (err) {
    return res.send("Error");
  }
});

app.post("/search", loggedin, async (req, res) => {
  const { searchTitle } = req.body;
  const userId = req.session.user;
  try {
    if (!checkTitle(searchTitle)) {
      return res.send("Invalid title");
    }
    if (userId !== adminUUID) {
      return res.send("Only admin can search for notes");
    }
  } catch (err) {
    return res.redirect(`/${userId}`);
  } finally {
    const notes = await filehound
      .create()
      .paths(`./notes/${adminUUID}`)
      .match(`*${searchTitle}*-*.txt`)
      .ext("txt")
      .find();
    return res.render("search", { data: { ...notes, id: userId } });
  }
});

app.get("/logout", (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.send("Error logging out");
    } else {
      return res.redirect("/login");
    }
  });
});

app.get("/report", loggedin, (req, res) => {
  return res.render("report");
});

app.post("/report", loggedin, (req, res) => {
  const { title, note } = req.body;
  visit(title, note, adminPass);
  return res.send("Reported");
});

app.get("/:uuid", loggedin, (req, res) => {
  if (req.session.user !== req.params.uuid) {
    return res.redirect(`/${req.session.user}`);
  }
  return res.render("home");
});

app.get("/shared/:noteid", loggedin, (req, res) => {
  try {
    const noteId = req.params.noteid;
    const sharedNote = getsharedNote(noteId);

    if (sharedNote && sharedNote.owner !== adminUUID) {
      const note = fs.readFileSync(
        `./notes/${sharedNote.owner}/${sanitize(
          sharedNote.title
        )}-${noteId}.txt`,
        "utf8"
      );
      return res.render("note", { content: btoa(note), ...sharedNote });
    }
    return res.send("Note not found.");
  } catch (err) {
    return res.send("Note not found.");
  }
});

app.get("/:uuid/:noteid", loggedin, (req, res) => {
  try {
    if (req.session.user !== req.params.uuid) {
      return res.redirect(`/${req.session.user}`);
    }

    const userId = req.params.uuid;
    const noteId = req.params.noteid;

    const userNote = getNote(noteId, userId);
    const note = fs.readFileSync(
      `./notes/${userId}/${sanitize(userNote.title)}-${noteId}.txt`,
      "utf8"
    );
    return res.render("note", { content: btoa(note), ...userNote });
  } catch (err) {
    return res.send("Note not found.");
  }
});

app.get("/:uuid/:noteid/delete", loggedin, (req, res) => {
  try {
    if (req.session.user !== req.params.uuid) {
      return res.redirect(`/${req.session.user}`);
    }
    const userId = req.params.uuid;
    const noteId = req.params.noteid;
    const userNote = getNote(noteId, userId);
    if (userNote && userNote.owner === adminUUID) {
      return res.send("You cannot delete admin's notes.");
    }
    deleteNote(noteId, userId);
    return res.redirect(`/${userId}`);
  } catch (err) {
    return res.send("Note not found.");
  }
});

app.get("/:uuid/:noteid/raw", loggedin, (req, res) => {
  try {
    const userId = req.params.uuid;
    const noteId = req.params.noteid;
    if (userId === adminUUID) {
      return res.send("No Raw for Admin's notes.");
    }

    const userNote = getNote(noteId, userId);
    const note = fs.readFileSync(
      `./notes/${userId}/${sanitize(userNote.title)}-${noteId}.txt`,
      "utf8"
    );
    return res.send(note);
  } catch (err) {
    return res.send("Note not found.");
  }
});

app.get("/:uuid/:noteid/share", loggedin, (req, res) => {
  try {
    if (req.session.user !== req.params.uuid) {
      return res.redirect(`/${req.session.user}`);
    }
    const userId = req.params.uuid;
    const noteId = req.params.noteid;
    const userNote = getNote(noteId, userId);
    if (userNote && userNote.owner === adminUUID) {
      return res.send("You cannot share admin's notes.");
    }
    const sharedNoteId = shareNote(noteId, userId);
    return res.redirect(`/shared/${sharedNoteId}`);
  } catch (err) {
    return res.send("Note not found.");
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
