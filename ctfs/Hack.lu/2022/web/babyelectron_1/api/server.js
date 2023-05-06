const express = require("express");
const http = require("http");

const sqlite3 = require("sqlite3").verbose();
const crypto = require("crypto");
const path = require("path");
var glob = require("glob");
var shortid = require('shortid');

var Fakerator = require("fakerator");
var fakerator = Fakerator("fr-FR"); // as close to LU as we can get

const BIND_ADDR = process.env.BIND_ADDR || "0.0.0.0";
const PORT = process.env.PORT || "1024";
const DB = 'db.db';

const app = express();
app.use(express.json());
const server = http.createServer(app);

const db = new sqlite3.Database(DB, (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the database.');
  db.exec("PRAGMA journal_mode = WAL;")
})

const sendResponse = (res, status, data) => {
  res.status(status).json(data);
  res.end();
};


images = []
glob("images/*.jpeg", function(err, _images){
  images = _images
})


// TBD: wait until some guy makes a nice async sqlite3 cuz we cba 

app.post("/register", (req, res) => {
  let username = req.body["username"] || "";
  let password = req.body["password"] || "";

  if (
    typeof username !== "string" ||
    typeof password !== "string" ||
    username.length === 0 ||
    password.length === 0 ||
    username.length > 50
  )
    return sendResponse(res, 400, { error: "Invalid request" });

  db.get("SELECT * FROM RELusers WHERE username = ?", username, (err, row) => {
    if (err) return sendResponse(res, 500, { error: "Failed to create user" });

    if (row) return sendResponse(res, 400, { error: "User already exists" });

    let passHash = crypto.createHash("sha256").update(password).digest("hex");
    let token = crypto.randomBytes(16).toString("hex");
    db.run(
      "INSERT INTO RELusers(username, password, token, money) VALUES(?, ?, ?, 1333337)",
      username,
      passHash,
      token,
      (err) => {
        if (err)
          return sendResponse(res, 500, { error: "Failed to create user" });

        return sendResponse(res, 200, { token: token });
      }
    );
  });
});

app.post("/login", (req, res) => {
  let username = req.body["username"] || "";
  let password = req.body["password"] || "";

  if (
    typeof username !== "string" ||
    typeof password !== "string" ||
    username.length === 0 ||
    password.length === 0 ||
    username.length > 50
  )
    return sendResponse(res, 400, { error: "Invalid request" });

  let passHash = crypto.createHash("sha256").update(password).digest("hex");
  db.get(
    "SELECT token, money from RELusers WHERE username = ? AND password = ?",
    username,
    passHash,
    (err, row) => {
      if (err)
        return sendResponse(res, 500, { error: "Failed to fetch token" });
      if (!row) return sendResponse(res, 401, { error: "Invalid credentials" });

      return sendResponse(res, 200, { token: row["token"], money: row["money"] });
    }
  );
});



function generateListings(num){
  data = []
  for(; data.length != num; ){
    data.push({
    price: parseInt(crypto.randomBytes(2).toString("hex"),16),
    name: fakerator.address.street(),
    message: fakerator.lorem.sentence(),
    sqm: parseInt(crypto.randomBytes(1).toString("hex"),16),
    image: images[Math.floor(Math.random() * images.length)],
    houseId: shortid.generate()
  })}

  return data
}

app.get("/listings", (req, res) => {
  let token = req.query.token?.toString() || "";
  let needed = 0; 

  db.get("SELECT * FROM RELusers where token = ?", token, (err,row) => {
    if(!row) {sendResponse(res, 500, {err: "Token does not belong to user"})}
    db.all("SELECT * FROM RELhouses WHERE offeredTo = ?", token, (err, rows) => {
      if (err)
        return sendResponse(res, 500, { err: "Internal server error"});

      needed = 3 - (rows?.length || 0)
      data = generateListings(needed)
  
      for (house of data){
        db.run(
          "INSERT INTO RELhouses(houseId, offeredTo, forSale, owner, price, name, message, sqm, picture) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
          house.houseId,
          token,
          true,
          null,
          house.price,
          house.name,
          house.message,
          house.sqm,
          house.image,
          (err) => {
            if (err)
              return sendResponse(res, 500, { error: "Failed to insert property" });
          });
      }
  
      for(row of rows){
        data.push({
          price: row.price,
          name: row.name,
          message: row.message,
          sqm: row.sqm,
          image: row.picture,
          houseId: row.houseId
        })
      }
      return sendResponse(res, 200, data)
  
    });
  })
  
});

app.post('/buy', (req, res) => {

  let token = req.body["token"] || ""
  let houseId = req.body["houseId"] || "";

  if (
    typeof token !== "string" ||
    typeof houseId !== "string" ||
    token.length === 0 ||
    houseId.length === 0
  )
    return sendResponse(res, 400, { error: "Invalid request" });

  db.get("SELECT price, id FROM RELhouses WHERE houseId = ? AND offeredTo = ?", houseId, token, (err, result) => {
    if(err){
      return sendResponse(res, 500, {error: "Internal Server Error"})
    }

    if(result){
      db.get("SELECT money from RELusers WHERE token = ?", token, (err, row) => {
        if(err){

          return sendResponse(res, 500, {error: "Could not retrieve funds from user"})
        }

        if(row){

          if(row["money"] >= result["price"]){
            //deduct money
            db.run("UPDATE RELusers SET money = ? WHERE token = ?", (row["money"] - result["price"]), token, (err, _) => {
              if(err){

                return sendResponse(res, 500, {error: "Could not deduct money"})
              }

              //update house
              db.run("UPDATE RELhouses SET owner = ?, offeredTo = ?, forSale = ? WHERE id = ?", token, null, false, result["id"], (err, _) => {
                if(err){

                  return sendResponse(res, 500, {error: "RIP Money"})
                }
  
                return sendResponse(res, 200, {success: true})
              })
            })
          }else{
            return sendResponse(res, 403, {error: "Not enough funds!"})
          }
        }
      })
    }else{
      return sendResponse(res, 400, {error: "Not Found"})
    }
  })
})

app.post('/sell', async (req, res) => {

  let token = req.body["token"] || ""
  let houseId = req.body["houseId"] || "";
  let message = req.body["message"] || "";
  let price = Number(req.body["price"]) || "";

  if (
    typeof token !== "string" ||
    typeof houseId !== "string" ||
    typeof message !== "string" ||
    token.length === 0 ||
    message.length === 0 ||
    houseId.length === 0
  )
    return sendResponse(res, 400, { error: "Invalid request" });

  db.get("SELECT * from RELhouses WHERE owner = ? AND houseId = ?", token, houseId,  (err, row) => {
    if(err){
      return sendResponse(res, 500, {error: "Internal Server error"})
    }
    if(row){
      db.run("UPDATE RELhouses SET forSale = 1, message = ?, price = ? WHERE houseId = ?", message, price, houseId, (err, _) => {
        if(err){
          return sendResponse(res, 500, {error: "Listing house for sale failed"})
        }
        return sendResponse(res, 200, {success: true})
      })
    }else{
      return sendResponse(res, 404, {error: "Not found"})
    }
  })
})

app.get('/portfolio', (req, res) => {

  let token = req.query.token?.toString() || "";

  if(
    token.length === ""
  ){
    return sendResponse(res, 400, { error: "Invalid Request" })
  }

  db.all("SELECT * from RELhouses where owner = ? AND forSale = 0", token, (err, rows) => {
    if(err){
      return sendResponse(res, 500, {error: "Internal Server Error"})
    }

    if(typeof rows !== undefined){
      let data = []
      for(row of rows){
        data.push({
          price: row.price,
          name: row.name,
          message: row.message,
          sqm: row.sqm,
          image: row.picture,
          houseId: row.houseId,
        })
      }
      return sendResponse(res, 200, data)
    }else{
      return sendResponse(res, 200, {})
    }
  });
})

app.post('/report', (req,res) => {

  let houseId = req.query.houseId || "";
  let message = req.body["message"] || "";

  if (
    typeof houseId !== "string" ||
    typeof message !== "string" ||
    houseId.length === 0 ||
    message.length === 0
  )
    return sendResponse(res, 400, { err: "Invalid request" });

  // allow only valid houseId's
  db.get("SELECT * from RELhouses WHERE houseId = ?", houseId, (err, house) => {
    if(house){
      let token = crypto.randomBytes(16).toString("hex");
      db.run(
        "INSERT INTO RELsupport(reportId, houseId, message, visited) VALUES(?, ?, ?, ?)",
        token,
        houseId,
        message,
        false,
        (err) => {
          if (err){
            return sendResponse(res, 500, { err: "Failed to file report" });
          }
          return sendResponse(res, 200, {msg: `Thank you for your Report!\nHere is your ID: ${token}`})  
        })
      }
    else{
      return sendResponse(res, 500, { err: "Failed to find that property" });
    }
  })
})

app.get('/support', (req,res) => {

  let reportId = req.query.reportId || "";
  if(
    typeof reportId !== "string" ||
    reportId.length === 0
  ){
    return sendResponse(res, 400, { err: "Invalid request" });
  }
  db.get("SELECT * from RELsupport WHERE reportId = ?", reportId, (err, row) =>{
    if(err){return sendResponse(res, 500, {err: err.stack})}
    if(row){
        db.run(
          "UPDATE RELsupport SET visited = 1 WHERE id = ?", row["id"], ()=>{
            db.get(
              "SELECT * from RELhouses WHERE houseId = ? AND forSale = 1", row["houseId"], (err, house) =>{
                if(err){
                    return sendResponse(res, 500, {err: "Internal Server Error"})
                }
                data = []
                data.push({
                  price: house.price,
                  name: house.name,
                  message: house.message,
                  sqm: house.sqm,
                  image: house.picture,
                  houseId: house.houseId,
                  msg: row["message"]
                })
                return sendResponse(res, 200, data)
              })
        })
      }else{
              return sendResponse(res, 200, {err: "No report with that ID"}) 
      }
  })
})

db.exec(
  `
  CREATE TABLE IF NOT EXISTS "RELusers"(
    "id" INTEGER PRIMARY KEY NOT NULL,
    "username" VARCHAR(50) NOT NULL,
    "password" VARCHAR(64) NOT NULL,
    "token" VARCHAR(32) NOT NULL,
    "money" INTEGER
  );
  CREATE TABLE IF NOT EXISTS "RELhouses"(
    "id" INTEGER PRIMARY KEY NOT NULL,
    "houseId" VARCHAR(20) NOT NULL,
    "offeredTo" VARCHAR(20), 
    "forSale" BOOLEAN NOT NULL,
    "owner" VARCHAR(20),
    "price" INTEGER NOT NULL,
    "name" VARCHAR(20),
    "message" VARCHAR(500),
    "sqm" INTEGER NOT NULL,
    "picture" VARCHAR(50)
  );

  CREATE TABLE IF NOT EXISTS "RELsupport"(
    "id" INTEGER PRIMARY KEY NOT NULL,
    "reportId" VARCHAR(20) NOT NULL,
    "houseId" VARCHAR(20) NOT NULL,
    "message" VARCHAR(500),
    "visited" BOOLEAN NOT NULL
  );
`,
  (err) => {
    if (err) {
      console.log(err);
      process.exit(1);
    }

    server.listen(PORT, BIND_ADDR, () => {
      console.log(`Running on ${BIND_ADDR}:${PORT}...`);
    });
  }
);
