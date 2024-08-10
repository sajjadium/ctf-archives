import express from "express";
import cookieParser from "cookie-parser";
import path from "path";
import fs from "fs";
import crypto from "crypto";

const accounts: [string, string][] = [];

const jwtSecret = "xook";
const jwtHeader = Buffer.from(
  JSON.stringify({ alg: "HS256", typ: "JWT" }),
  "utf-8"
)
  .toString("base64")
  .replace(/=/g, "");

const sign = (payload: object) => {
  const jwtPayload = Buffer.from(JSON.stringify(payload), "utf-8")
    .toString("base64")
    .replace(/=/g, "");
    const signature = crypto.createHmac('sha256', jwtSecret).update(jwtHeader + '.' + jwtPayload).digest('base64').replace(/=/g, '');
  return jwtHeader + "." + jwtPayload + "." + signature;

}

const app = express();

const port = process.env.PORT || 3000;

app.listen(port, () =>
  console.log("server up on http://localhost:" + port.toString())
);

app.use(cookieParser());
app.use(express.urlencoded({ extended: true }));

app.use(express.static(path.join(__dirname, "site")));

app.get("/flag", (req, res) => {
  if (!req.cookies.token) {
    console.log('no auth')
    return res.status(403).send("Unauthorized");
  }

  try {
    const token = req.cookies.token;
    // split up token
    const [header, payload, signature] = token.split(".");
    if (!header || !payload || !signature) {
      return res.status(403).send("Unauthorized");
    }
    Buffer.from(header, "base64").toString();
    // decode payload
    const decodedPayload = Buffer.from(payload, "base64").toString();
    // parse payload
    const parsedPayload = JSON.parse(decodedPayload);
		// verify signature
		const expectedSignature = crypto.createHmac('sha256', jwtSecret).update(header + '.' + payload).digest('base64').replace(/=/g, '');
		if (signature !== expectedSignature) {
			return res.status(403).send('Unauthorized ;)');
		}
    // check if user is admin
    if (parsedPayload.admin || !("name" in parsedPayload)) {
      return res.send(
        fs.readFileSync(path.join(__dirname, "flag.txt"), "utf-8")
      );
    } else {
      return res.status(403).send("Unauthorized");
    }
  } catch {
    return res.status(403).send("Unauthorized");
  }
});

app.post("/login", (req, res) => {
  try {
    const { username, password } = req.body;
    if (!username || !password) {
      return res.status(400).send("Bad Request");
    }
    if (
      accounts.find(
        (account) => account[0] === username && account[1] === password
      )
    ) {
      const token = sign({ name: username, admin: false });
      res.cookie("token", token);
      return res.redirect("/");
    } else {
      return res.status(403).send("Account not found");
    }
  } catch {
    return res.status(400).send("Bad Request");
  }
});


app.post('/signup', (req, res) => {
  try {
    const { username, password } = req.body;
    if (!username || !password) {
      return res.status(400).send('Bad Request');
    }
    if (accounts.find(account => account[0] === username)) {
      return res.status(400).send('Bad Request');
    }
    accounts.push([username, password]);
    const token = sign({ name: username, admin: false });
    res.cookie('token', token);
    return res.redirect('/');
  } catch {
    return res.status(400).send('Bad Request');
  }
});