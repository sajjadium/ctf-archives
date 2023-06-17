/*

1. Packages are the latest.
   (as of June 2023)

2. This is a ChatGPT-oriented code.
   (Ref. https://twitter.com/brokenpacifist/status/1650955597414809600)

3. https://fe.gy/ stores copyright-free music data.
   Attacking the infrastructure (includes DDoS, dirbusting, etc.) is strictly prohibited.

*/

// the "cheese"
process.env.NODE_ENV = "production"
const SECRET = process.env.SECRET || "CHEESE_SECRET"
const FLAG = process.env.FLAG || "codegate2023{some sameple flag for you}"
const REDIS_URL_CACHE = process.env.REDIS_URL_CACHE || "redis://127.0.0.1:6379/0"
const REDIS_URL_QUERY = process.env.REDIS_URL_QUERY || "redis://127.0.0.1:6379/1"
const STATIC_HOST = process.env.STATIC_HOST || "http://localhost:5000/"
const DIFFICULTY = process.env.DIFFICULTY || 7
const APP_HOST = process.env.APP_HOST || "0.0.0.0"
const APP_PORT = process.env.APP_PORT || 5000

// express
const axios = require("axios")
const dns = require("dns")
const express = require("express")
const fs = require("fs")
const ip = require("ip")
const session = require("express-session")
const Redis = require("ioredis")
const crypto = require("crypto")
const cookieParser = require("cookie-parser")

// streaming contents
const contentList = fs.readFileSync("list.xml", { encoding: "utf8", flag: "r" })
const allowedContentTypes = ["audio/mpeg", "audio/mp3", "audio/wav", "audio/ogg"]

// basic express setup
const app = express()
app.use(express.json())
app.use(cookieParser())
app.disable("x-powered-by")
app.set("title", "CODEGATE Music Player API")
app.set("view engine", "ejs")
app.use(session({
    secret: SECRET + FLAG,
    resave: true,
    saveUninitialized: true,
    cookie: {
        secure: false
    }
}))

// basic db setup
const redisCache = new Redis(REDIS_URL_CACHE)
const redisQuery = new Redis(REDIS_URL_QUERY)

// get last n characters of md5 result
const getLastCharacterMD5 = (s, n) => {
    const md5Hash = crypto.createHash("md5").update(s).digest("hex")
    const lastNCharacters = md5Hash.slice(-n)
    return lastNCharacters
}

// generate random string
const generateRandomString = (length) => {
    const characters = "abcdef0123456789"
    let result = ""

    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length)
        result += characters.charAt(randomIndex)
    }

    return result
}

// unified send to reduce code lines
const sendResponse = (res, message, status=200) => {
    res.status(status)
    res.write(message)
    res.send()
}

// check internal ip
const isInternalIP = (ipAddress) => {
    return ip.isPrivate(ipAddress)
}

// get ip address
const getIPAddress = (domain) => {
    return new Promise((resolve, reject) => {
        dns.lookup(domain, (error, addresses) => {
            if (error) {
                resolve(domain)
            } else {
                resolve(addresses)
            }
        })
    })
}

// fetch streaming
app.get("/api/list", (req, res) => {
    return sendResponse(res, contentList)
})

// run streaming
app.get("/api/stream/:url", (req, res) => {

    try {
        let url = req.params.url
        const domain = new URL(url).hostname

        // prevent memory overload
        redisCache.dbsize((err, result) => {
            if(result >= 256){
                redisCache.flushdb()
            }
        })

        // preventing DNS attacks, etc.
        getIPAddress(domain)
            .then(ipAddress => {
                if(!url.startsWith("http://") && !url.startsWith("https://")){
                    url = STATIC_HOST.concat(url).replace("..", "").replace("%2e%2e", "").replace("%2e.", "").replace(".%2e", "")
                }else{
                    if(isInternalIP(ipAddress)) return sendResponse(res, "No Hack!", 500)
                }

                // redis || axios
                redisCache.get(url.split("?")[0], (err, result) => {
                    if (err || !result){
                        axios
                            .get(url, { responseType: "arraybuffer", timeout: 3000 })
                            .then(response => {
                                if (!allowedContentTypes.includes(response.headers["content-type"])){
                                    return sendResponse(res, "Not a valid music file", 500)
                                }
                                if (response.data.byteLength >= 1024 * 1024 * 3) {
                                    return sendResponse(res, "Music file is too big", 500)
                                }
                                redisCache.set(url, response.data.toString("hex"))
                                console.log(url)
                                return sendResponse(res, response.data)
                            })
                            .catch(err => {
                                return sendResponse(res, "No Hack!", 500)
                            })
                    }else{
                        return sendResponse(res, Buffer.from(result, "hex"))
                    }
                })
            })
            .catch(e => {
                return sendResponse(res, "No Hack!", 500)
            })
    } catch (err) {
        return sendResponse(res, "Failed Streaming!", 500)
    }
})

// inquiry
app.get("/api/inquiry", (req, res) => {
    if(!req.session.lastValue || !req.session.lastLength){
        req.session.lastLength = DIFFICULTY
        req.session.lastValue = generateRandomString(DIFFICULTY)
        return sendResponse(res, `${req.session.lastLength}/${req.session.lastValue}`)
    }

    if(!req.query.url || typeof req.query.url !== "string"){
        return sendResponse(res, "No Hack!", 500)
    }

    if(!req.query.checksum || getLastCharacterMD5((req.query.checksum || ''), DIFFICULTY) !== req.session.lastValue){
        req.session.lastLength = DIFFICULTY
        req.session.lastValue = generateRandomString(DIFFICULTY)
        return sendResponse(res, `${req.session.lastLength}/${req.session.lastValue}`, 500)
    }

    redisQuery.rpush("query", req.query.url)
    req.session.lastLength = DIFFICULTY
    req.session.lastValue = generateRandomString(DIFFICULTY)

    return sendResponse(res, "Complete")
})

// inquiry
app.post("/api/messages", (req, res) => {
    const { id } = req.body
    if (!req.cookies["SECRET"] || req.cookies["SECRET"] !== SECRET) {
        return sendResponse(res, "Nope", 403)
    }
    return res.render("admin", {...id})
})

// get flag
app.patch("/api/flag", (req, res) => {
    const { flag } = req.body
    if (!req.cookies["SECRET"] || req.cookies[SECRET] !== FLAG) {
        return sendResponse(res, "Nope", 403)
    }
    return res.render("flag", flag)
})

// 404
app.get("*", (req, res) => {
    return sendResponse(res, "404", 404)
})

// start
const start = async () => {
    try {
        await app.listen(APP_PORT, APP_HOST)
    } catch(err) {
        app.log.error(err)
        process.exit(1)
    }
}

start()
