const express = require("express");
const app = express();
const baseRouter = require("./routes/baseRouter.js");
const chatRouter = require("./routes/chatRouter.js");
const videoRouter = require("./routes/videoRouter.js");
const cookieParser = require('cookie-parser');
const security = require("./middlewares/security")
require('express-ws')(app);
//const {adminSeeVideo} = require("bot")

app.use(cookieParser());
app.use(express.json({limit: '10mb'}));

//await adminSeeVideo.start();

//if dev needs to debug
if (process.env.NODE_ENV === "production") {
    app.set("trust proxy", 1);
    app.use(function (req, res, next) {
        res.setHeader("Access-Control-Allow-Origin", process.env.FRONTEND);
    
        res.setHeader(
        "Access-Control-Allow-Methods",
        "GET, POST, PUT"
        );
        
        res.setHeader("Access-Control-Allow-Headers", "Content-Type");
        res.setHeader("Access-Control-Allow-Credentials", true);
    
        next();
    });
}

app.use("/api",baseRouter);
app.use("/api/chats",chatRouter);
app.use("/api/videos",videoRouter);

app.listen(3000, async()=>{console.log("App is listening on port 3000")});
