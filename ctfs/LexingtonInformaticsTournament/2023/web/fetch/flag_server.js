import express from "express";

const app = express();
const port = 6969;
export const randomString = Math.random().toString(36).substring(7);
app.get("/" + randomString, (req, res) => res.sendFile("flag.txt"));
export const startFlagServer = () =>
  app.listen(port, "127.0.0.1", () =>
    console.log(`flag server listening on port ${port}!`)
  );
