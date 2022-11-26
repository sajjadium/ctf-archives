const express = require("express");
const bodyParser = require("body-parser");
const { inviteCode, flag } = require("./secret");
const app = express();

app.use(bodyParser.text());
const port = process.env.PORT || 3000;
const baseUser = { picture: "default.png" };

function createAdmin() {
  return `Creating admin account, flag is ${flag}`;
}
function createUser() {
  return "Creating user account";
}

app.post("/", (req, res) => {
  let user;
  try {
    user = JSON.parse(req.body);
  } catch (e) {
    return res.status(400).json({ message: "Invalid Request body" });
  }
  if (user.isAdmin && user.inviteCode !== inviteCode) {
    res.send("No invite code? No admin!");
  } else {
    let newUser = Object.assign(baseUser, user);
    if (newUser.isAdmin) {
      res.send(createAdmin(newUser));
    } else {
      res.send(createUser(newUser));
    }
  }
});
app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});
