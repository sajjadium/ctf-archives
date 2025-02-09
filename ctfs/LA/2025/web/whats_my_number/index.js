const express = require("express");
const path = require("path");
const fs = require("fs");
const http = require("http");

const app = express();
const PORT = process.env.PORT || 3000;

const SPAM_PERIOD = 40;

let total_guesses = 0;

function getRandom() {
  return Math.floor(Math.random() * 1e9);
}

app.use(express.static(path.join(__dirname, "../public")));

// Endpoint to get a random number
app.get("/api/random", (req, res) => {
  const randomNumber = getRandom();
  res.json({ randomNumber });
});

// Endpoint to guess a number
app.get("/api/guess", (req, res) => {
  const guess = req.query.num;
  let guess_num;

  total_guesses += 1;

  try {
    guess_num = parseInt(guess);
  } catch (error) {
    console.error("Could not parse guess:", guess);
    res.status(500).json({ error: "Could not parse guess" });
    return;
  }

  if (isNaN(guess_num)) {
    console.error("Could not parse guess:", guess);
    res.status(500).json({ error: "Could not parse guess" });
    return;
  }

  let test_num = getRandom();

  if (test_num === guess_num) {
    fs.readFile(path.join(__dirname, "../flag.txt"), "utf-8", (err, flag) => {
      if (err) {
        console.error("Failed to read flag file", err);
        res.status(500).json({
          error: "Error reading flag file, please contact CTF organizers",
        });
        return;
      }
      const response_msg = flag;
      res.json({ response_msg, total_guesses });
    });
  } else {
    let response_msg = "Wrong number! The right number is: " + test_num;
    res.json({ response_msg, total_guesses });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

// Spam requests to the server at some fixed interval
// Use a persistent http session
let failed_requests = 0;

const start_spamming = () => {
  console.log("Starting spam requests");

  const agent = new http.Agent({ keepAlive: true });

  const send_request = () => {
    const options = {
      hostname: "localhost",
      port: PORT,
      path: "/api/random",
      method: "GET",
      agent: agent,
    };

    const req = http.request(options, (res) => {
      let data = "";

      res.on("data", (chunk) => {
        data += chunk;
        failed_requests = 0;
      });
    });

    req.on("error", (error) => {
      console.error("Request error: ", error);
      failed_requests++;

      // If 10 requests in a row fail, exit the program; something is wrong
      if (failed_requests >= 10) {
        console.error("Too many requests failing! Exiting program.");
        process.exit(1);
      }
    });

    req.end();
  };

  setInterval(send_request, SPAM_PERIOD);
};

setTimeout(start_spamming, 500);
