
import {config} from "dotenv";
config();

import fs from "fs";
import path from "path";

import {quote} from "shell-quote";
import {exec} from "child_process";

const textsDir = path.join(process.cwd(), "public", "texts");
const uwuifierPath = path.join(process.cwd(),"uwuify");

import express from "express";
const app = express();

import morgan from "morgan";
app.set('trust proxy', ['loopback', 'linklocal', 'uniquelocal']);
app.use(morgan("combined"));

app.get("/", (req, res) => {
  res.sendFile("public/index.html", {
    root: process.cwd() // bug fix
  });
});


app.get("/uwuify", (req, res) => {
  res.type("txt");
  if(req.query.src){
    if(req.query.src.includes("..") || req.query.src.includes("./") || req.query.src.startsWith("/") || req.query.src.startsWith("-")){
      res.send("no hacking >:(");
      res.end();
      return;
    }
    let cmd = "cat " + quote([req.query.src]) + " | " + uwuifierPath;
    exec(cmd, {
      cwd: textsDir
    }, (err, stdout, stderr) => {
      res.send(stdout + stderr);
      res.end();
    });
  }else{
    res.send("no src provided");
  }
});

app.get("/dir", async (req, res) => {
    res.type("txt");
    let output = "texts avali to uwuify: ";
    let files = await fs.promises.readdir(textsDir);
    for(let file of files){
        output += "\r\n" + file;
    }
    output += "\r\n\r\nUse /uwuify?src=<text file name> to uwuify a text file!";
    res.send(output);
});

app.listen(process.env.PORT || 3000, () => {
  console.log("Server Up!");
});
