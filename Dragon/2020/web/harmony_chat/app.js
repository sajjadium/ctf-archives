const express = require("express")
const websocket = require("ws")
const http = require("http")
const path = require("path")
const ftpd = require("ftpd")
const EventEmitter = require("events")

const utils = require("./utils")
const logfs = require("./logfs")
const harmony = require("./harmony")
const ContentSecurityPolicy = require("./csp")

const HTTP_PORT = process.env.HTTP_PORT || 3380
const FTP_PORT = process.env.FTP_PORT || 3321
const FTP_IP = process.env.FTP_IP || "192.168.2.199"
const FTP_PASV_PORT_START = process.env.FTP_PASV_PORT_START || 10000
const FTP_PASV_PORT_END = process.env.FTP_PASV_PORT_END || 50000

const harmonyApp = express()
const httpServer = http.createServer(harmonyApp)
const wsServer = new websocket.Server({
  noServer: true
})

const PACKET_SCHEMA = {
  "type": "object",
  "properties": {
    "type": {
      "enum": [
        "login",
        "register",
        "new-channel",
        "message",
        "invite"
      ]
    },
  },
  "required": [
    "type"
  ],
  "anyOf": [
    {
      "properties": {
        "type": { "const": "login" },
        "uid": {
          "type": "string",
          "pattern": "^[0-9a-f]{32}$"
        }
      },
      "required": [ "uid" ],
      "additionalProperties": false
    },
    {
      "properties": {
        "type": { "const": "register" },
        "displayName": {
          "type": "string",
          "pattern": "^[A-Za-z0-9 ~`!@#$%^&*()_+=\\[\\]{};':\"\\\\|,./<>?-]{1,30}$"
        }
      },
      "required": [ "displayName" ],
      "additionalProperties": false
    },
    {
      "properties": {
        "type": { "const": "new-channel" },
        "name": {
          "type": "string",
          "pattern": "^[A-Za-z0-9-]{1,30}$"
        }
      },
      "required": [ "name" ],
      "additionalProperties": false
    },
    {
      "properties": {
        "type": { "const": "message" },
        "msg": {
          "type": "string",
          "pattern": "^[^\\r\\n]{0,2048}$"
        },
        "chId": {
          "type": "string",
          "pattern": "^[0-9a-f]{32}$"
        }
      },
      "required": [ "msg", "chId" ],
      "additionalProperties": false
    },
    {
      "properties": {
        "type": { "const": "invite" },
        "uid": {
          "type": "string",
          "pattern": "^[0-9a-f]{32}$"
        },
        "chId": {
          "type": "string",
          "pattern": "^[0-9a-f]{32}$"
        }
      },
      "required": [ "uid", "chId" ],
      "additionalProperties": false
    }
  ]
}

const harmonyUsers = new Map()
const harmonyChannels = new Map()

harmonyApp.use(ContentSecurityPolicy)
harmonyApp.use(express.static("static"))

harmonyApp.get("/logs/:uid([0-9a-f]{32})/:chId([0-9a-f]{32})", (req, res) => {
  const user = harmonyUsers.get(req.params.uid)
  if (!user) {
    res.status(404).send("Error: User not found.")
    return
  }

  const channel = harmonyChannels.get(req.params.chId)
  if (!channel) {
    res.status(404).send("Error: Channel not found.")
    return
  }

  if (!channel.present.has(user.id)) {
    res.status(404).send("Error: User isn't present on this channel.")
    return
  }

  res.set("Content-Type", "text/plain")
  res.send(channel.getLogs())
})

harmonyApp.get("/logs/:uid([0-9a-f]{32})", (req, res) => {
  const user = harmonyUsers.get(req.params.uid)
  if (!user) {
    res.status(404).send("Error: User not found.")
    return
  }

  const links = []
  user.channelsPresent.forEach(channel => {
    links.push(`<a href="/logs/${user.id}/${channel.id}">${channel.id}</a>`)
  })

  res.send(
    `<html><body><h3>Channels:</h3><pre>${links.join("\n")}</pre></body></html>`
  )
})

httpServer.on("upgrade", (req, s, head) => {
  if (req.url !== "/chat") {
    s.write(
        "HTTP/1.1 404 Not Found\r\n" +
        "Content-Type: text/plain\r\n" +
        "\r\n" +
        "Not found"
    )
    return
  }

  wsServer.handleUpgrade(req, s, head, (ws) => {
    wsServer.emit("connection", ws, req)
  })
})

wsServer.on("error", error => {
  console.warn("wsServer error:", error)
})

wsServer.on("connection", (ws, req) => {
  let user = null

  const helperSendError = text => {
    ws.send(JSON.stringify({ type: "error", msg: text }))
  }

  const helperSendMessage = text => {
    ws.send(JSON.stringify({ type: "server", msg: text }))
  }

  ws.on("message", data => {
    let msg = null
    try {
      msg = utils.validateAndDecodeJSON(data, PACKET_SCHEMA)
    } catch (error) {
      if (ws.readyState === 1) {
        helperSendError("Protocol Error: " + error)
      }
      console.warn(error)
      return
    }

    switch (msg.type) {
      case "login":
        if (user) {
          helperSendError("Error: already logged in.")
        } else {
          const candidateUser = harmonyUsers.get(msg.uid)
          if (candidateUser) {
            user = candidateUser
            user.ws = ws
            user.sendUserId()
            helperSendMessage(`Logged in as ${user.displayName}!`)
            user.sendAllChannels()
            console.log(`Login: ${user.id} - ${user.displayName}`)
          } else {
            helperSendError(
              "Error: invalid uid (register first to get your uid)"
            )
          }
        }
        break

      case "register":
        if (user) {
          helperSendError("Error: can't register if you're already logged in.")
        } else {
          user = new harmony.User(msg.displayName)
          user.ws = ws
          harmonyUsers.set(user.id, user)
          user.sendUserId()
          helperSendMessage(
              `Registered and logged in! Your UID is ${user.id} - save it!`
          )
          console.log(`New user: ${user.id} - ${user.displayName}`)
        }
        break

      case "new-channel":
        if (!user) {
          helperSendError("Error: please login first.")
          break
        }

        if (user.channelsOwned.size >= 10) {
          helperSendError("Error: you can't own more than 10 channels.")
          break
        }

        const newChannel = new harmony.Channel(msg.name, user)
        harmonyChannels.set(newChannel.id, newChannel)
        break

      case "message":
        if (user) {
          const channel = harmonyChannels.get(msg.chId)
          if (channel) {
            channel.postMessage(user, msg.msg)
          } else {
            helperSendError("Error: unknown channel.")
          }

        } else {
          helperSendError("Error: please login first.")
        }
        break

      case "invite":
        if (!user) {
          helperSendError("Error: please login first.")
          break
        }

        const channel = harmonyChannels.get(msg.chId)
        if (!channel) {
          helperSendError("Error: unknown channel.")
          break
        }

        const invitedUser = harmonyUsers.get(msg.uid)
        if (!invitedUser) {
          helperSendError("Error: unknown user.")
          break
        }

        channel.joinUser(invitedUser)
        helperSendMessage(
            `Invited ${invitedUser.displayName} to channel ${channel.name}.`
        )
        break
    }
  })

  ws.on("close", () => {
    if (user) {
      user.ws = null
    }
  })
})

httpServer.listen(HTTP_PORT, "0.0.0.0", () => {
  console.log(`Harmony HTTP server started at port ${HTTP_PORT}`)
})

const ftpServer = new ftpd.FtpServer(FTP_IP, {
  getInitialCwd: conn => "/",
  getRoot: conn => "/",
  pasvPortRangeStart: FTP_PASV_PORT_START,
  pasvPortRangeEnd: FTP_PASV_PORT_END,
  useWriteFile: false,
  useReadFile: true,
  maxStatsAtOnce: 1
})

ftpServer.on("error", error => {
  console.log(`FTP error: ${error}`)
})

ftpServer.on("client:connected", conn => {
  let user = null

  conn.on("command:user", (uid, succeed, fail) => {
    const candidateUser = harmonyUsers.get(uid.trim())
    if (!candidateUser) {
      fail()
      return
    }

    user = candidateUser
    succeed()
  })

  conn.on("command:pass", (pass, succeed, fail) => {
    // Accept any password.
    console.log(`FTP login: ${user.id} - ${user.displayName}`)
    const chatLogFS = new logfs.ChatLogFS(user)
    succeed(user.id, chatLogFS)
  })
})

const originalLogIf = ftpServer._logIf
//ftpServer.debugging = 0
ftpServer.listen(FTP_PORT)
ftpServer._logIf = (verbosity, message, conn) => {
  const ignoreList = [
    "Non-passive data connection ended",
    "Data connection error: Error: connect ECONNREFUSED"
  ]

  if (ignoreList.some(substring => message.includes(substring))) {
    return
  }

  return originalLogIf.call(ftpServer, verbosity, message, conn)
}
console.log(`Harmony FTP server started at port ${FTP_PORT}`)

process.on('uncaughtException', (err, origin) => {
  console.error(
    `Caught unhandled exception: ${err}\n` +
    `Exception origin: ${origin}`
  )
})

