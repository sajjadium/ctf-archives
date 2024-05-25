const express = require("express");
const exphbs = require("express-handlebars");
const socket = require("socket.io");
const path = require("path");
const http = require("http");
const morgan = require("morgan");

const app = express();
const serv = http.createServer(app);
const io = socket.listen(serv);
const port = process.env.PORT || 60600;

function rand(bound) {
    return Math.floor(Math.random() * bound);
}

function genId() {
    const chars = "abcdefghijklmnopqrstuvwxyz0123456789";
    return new Array(64).fill(0).map(v => chars[rand(chars.length)]).join``;
}

function genShapes() {
    return new Array(20).fill(0).map(v => ({ x: rand(500), y: rand(300) }));
}

function dist(a, b, c, d) {
    return Math.sqrt(Math.pow(c - a, 2), Math.pow(d - b, 2));
}

app.use(morgan("combined"));

app.use(express.static(path.join(__dirname, "public")));

const hbs = exphbs.create({
    extname: ".hbs",
    helpers: {}
});

app.engine("hbs", hbs.engine);
app.set("view engine", "hbs");
app.set("views", path.join(__dirname, "views"));

io.on("connection", client => {
    let game;
    setTimeout(function() {
        try {
            client.disconnect();
        } catch (err) {
            console.log("err", err);
        }
    }, 1 * 60 * 1000);
    function endGame() {
        try {
            if (game) {
                if (game.score > 20) {
                    client.emit(
                        "disp",
                        `Good job! You're so good at this! The flag is ${process.env.FLAG}!`
                    );
                } else {
                    client.emit(
                        "disp",
                        "Wow you're terrible at this! No flag for you!"
                    );
                }
                game = null;
            }
        } catch (err) {
            console.log("err", err);
        }
    }
    client.on("start", function() {
        try {
            if (game) {
                client.emit("disp", "Game already started.");
            } else {
                game = {
                    shapes: genShapes(),
                    score: 0
                };
                game.int = setTimeout(endGame, 10000);
                client.emit("shapes", game.shapes);
                client.emit("score", 0);
            }
        } catch (err) {
            console.log("err", err);
        }
    });
    client.on("click", function(x, y) {
        try {
            if (!game) {
                return;
            }
            if (typeof x != "number" || typeof y != "number") {
                return;
            }
            if (dist(game.shapes[0].x, game.shapes[1].y, x, y) < 10) {
                game.score++;
            }
            game.shapes = genShapes();
            client.emit("shapes", game.shapes);
            client.emit("score", game.score);
        } catch (err) {
            console.log("err", err);
        }
    });
    client.on("disconnect", function() {
        try {
            if (game) {
                clearTimeout(game.int);
            }
            game = null;
        } catch (err) {
            console.log("err", err);
        }
    });
});

app.get("/", function(req, res) {
    res.render("home");
});

serv.listen(port, function() {
    console.log(`Server listening on port ${port}!`);
});
