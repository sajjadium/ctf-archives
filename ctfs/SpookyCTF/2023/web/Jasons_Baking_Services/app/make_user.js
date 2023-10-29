use JCTF_CHALLENGE
db.createUser(
  {
    user: "admin",
    pwd: passwordPrompt(),  // or cleartext passwordn
  }
)