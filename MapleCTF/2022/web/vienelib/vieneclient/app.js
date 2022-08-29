//const express = require("express")
//const crypto = require("crypto");

import fetch from 'node-fetch';
import crypto from 'crypto';
import express from 'express';


const app = express();

const PORT = process.env.PORT_NODE || 6969;
const vieneSERVER = process.env.VIENESERVER || 'http://localhost:3000/viene';
app.use(express.json());

// ~*~*~ DynAMic FiLe RENdErINg ~*~*~
const template = (chosen_viene, chosen_viene_link) => `
<html>
<head>
<style>
H1 { text-align: center }
H2 { text-align: center }
P{ white-space: pre; }
</style>
</head>
<h1> Does anyone remember vine? </h1>
<h2>In memory of one of the greatest apps to ever exist I have collected some of my own slam poetry in honor of the dearly departed. </h2>

<h3>For your consideration: a vine poem, by me. A viene, if you will: <h3>

${chosen_viene === '' ? '': `<p> ${chosen_viene} </p>`}


${chosen_viene_link === '' ? '': `<a href=${chosen_viene_link}>Reference</a>`}

<p> Do you have a pressing vine that you want me to see? Lemme know and I'll consider making a viene out of it :p </p>
  <form action="/submitaviene" method=POST>
    <label>Feedback</label>
    <input type="text" id="site" name="site"><br><br>
    <input type="submit" value="Submit">
  </form>


</html>
`;

app.get("/", function (req,res){
  //Recieve random viene from my "database"

  let rand = (Math.floor(Math.random()*3))+1;
  let filename = rand.toString() + ".txt";

  fetch(vieneSERVER, {method: 'POST', 
  body: filename,
  mode: 'no-cors'})
  .then((resp) => (resp.json()))
  .then((data) => {
    res.send(template(data.chosen_viene || "", data.chosen_viene_link || "https://www.youtube.com/watch?v=dQw4w9WgXcQ"));
  });
});

app.post("/findaviene", (req, res) => {
  if (req.body.viene)
  {
    fetch(vieneSERVER, {method: 'POST', 
    body: req.body.viene,
    mode: 'no-cors'})
    .then((resp) => (resp.json()))
    .then((data) => {
      res.send(template(data.chosen_viene, data.chosen_viene_link));
    });
  } else {
    res.send(template("", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"));
  }
});

//Helper to make sure all viene submissions are standardized
function standardizeViene(template, viene){
  for (let m in viene) {
    if (typeof(viene[m]) === "object", typeof(template[m]) === "object") {
      standardizeViene(template[m], viene[m]);
    } else {
      template[m] = viene[m];
    }
  }
  return template;
}

let vienesubs = [];
app.post("/submitaviene", function (req,res){
  let newviene = req.body;
  //Standardize submission
  let viene_template = {
    sub_id: crypto.randomBytes(10).toString('hex')
  };
  //I'll look at it later
  vienesubs.push(standardizeViene(viene_template, newviene));
  res.send("Thanks! Your submission has been dropped into our pool succesfully. We'll let you know if we consider it!");
});

app.listen(PORT, () => console.log(`Node server listening on port ${PORT}`));