"use strict"

const FTP_PORT = 3321

class ChatWindow {
  elChat
  elChannelList
  elChannelName
  elChannelId

  elButtonChannelNew
  elButtonInvite
  elButtonLogsHTTP
  elButtonLogsFTP
  elButtonSend

  elInputChannelNew
  elInputInvite
  elInputChat

  templateChannel
  templateMsg
  templateServerMsg

  callbacks

  constructor() {
    this.elChat = document.getElementById("chat")
    this.elChannelList = document.getElementById("channel-list")
    this.elChannelName = document.getElementById("channel-name")
    this.elChannelId = document.getElementById("channel-id")

    this.elButtonChannelNew = document.getElementById("channel-new")
    this.elButtonInvite = document.getElementById("invite")
    this.elButtonLogsHTTP = document.getElementById("logs-http")
    this.elButtonLogsFTP = document.getElementById("logs-ftp")
    this.elButtonSend = document.getElementById("send-input")

    this.elInputChannelNew = document.getElementById("channel-new-name")
    this.elInputInvite = document.getElementById("invite-uid")
    this.elInputChat = document.getElementById("input")
    this.elInputChat.focus()

    this.templateChannel =
        document.getElementById("template-channel-list-item").content

    this.templateServerMsg =
        document.getElementById("template-server-msg").content

    this.templateErrorMsg =
        document.getElementById("template-error-msg").content

    this.templateMsg = document.getElementById("template-msg").content

    this.callbacks = new Map

    this.attachHandlers(
        "channel:new", this.elInputChannelNew, this.elButtonChannelNew
    )

    this.attachHandlers(
        "user:invite", this.elInputInvite, this.elButtonInvite
    )

    this.attachHandlers(
        "chat:send", this.elInputChat, this.elButtonSend
    )

    this.elButtonLogsHTTP.addEventListener("click", e => {
      this.emit("logs:http")
    })

    this.elButtonLogsFTP.addEventListener("click", e => {
      this.emit("logs:ftp")
    })

    this.reset()
  }

  on(event, callback) {
    this.callbacks.set(event, callback)
  }

  reset() {
    this.elChannelList.innerHTML = ""
    this.elChannelName.textContent = ""
    this.elChannelId.textContent = ""
    this.resetChat()
  }

  resetChat() {
    this.elChat.innerHTML = ""
  }

  switchToChannel(name, chId, messages) {
    this.elChannelName.textContent = name
    this.elChannelId.textContent = chId
    this.resetChat()

    const fragMessages = document.createDocumentFragment()

    messages.forEach(msg => {
      fragMessages.appendChild(
        this.createChatMessageFragment(msg)
      )
    })

    this.elChat.appendChild(fragMessages)
    this.scrollChatToBottom()
  }

  addChatMessage(msg) {
    this.elChat.appendChild(
      this.createChatMessageFragment(msg)
    )
    this.scrollChatToBottom()
  }

  setChannelList(channels) {
    this.elChannelList.innerHTML = ""
    const fragChannels = document.createDocumentFragment()

    channels.forEach(channel => {
      fragChannels.appendChild(
        this.createChannelFragment(channel.name, channel.chId)
      )
    })

    this.elChannelList.appendChild(fragChannels)
  }

  addChannelToList(name, chId) {
    this.elChannelList.appendChild(
      this.createChannelFragment(name, chId)
    )
  }

  createChannelFragment(name, chId) {
    const fragChannel = this.templateChannel.cloneNode(true)
    const elListItem = fragChannel.querySelectorAll("li")[0]
    elListItem.textContent = name
    elListItem.dataset.chId = chId

    elListItem.addEventListener("click", () => {
      this.emit("channel:switch", chId)
    })

    return fragChannel
  }

  scrollChatToBottom() {
    const elContainer = this.elChat.parentNode
    elContainer.scrollTop = elContainer.scrollHeight
  }

  createChatMessageFragment(msg) {
    const template = (msg.type === "server" ? this.templateServerMsg :
                      msg.type === "error"  ? this.templateErrorMsg :
                                              this.templateMsg)
    const fragMsg = template.cloneNode(true)

    const elName = fragMsg.querySelectorAll(".msg-name")[0]
    const elDate = fragMsg.querySelectorAll(".msg-date")[0]
    const elText = fragMsg.querySelectorAll(".msg-text")[0]

    if (elName) {
      elName.textContent = msg.name
    }

    if (elDate) {
      elDate.textContent = msg.date
    }

    if (elText) {
      elText.textContent = msg.text
    }

    return fragMsg
  }

  emit(event, ...args) {
    const callback = this.callbacks.get(event)
    if (callback) {
      callback(...args)
    } else {
      throw `Error: no handler for event '${event}'`
    }
  }

  attachHandlers(event, elInput, elButton) {
    const handler = () => {
      const val = elInput.value
      elInput.value = ""
      this.elInputChat.focus()  // Always refocus on message input.
      this.emit(event, val)
    }

    elInput.addEventListener("keydown", e => {
      if (e.code === "Enter" || e.code === "NumpadEnter") {
        handler()
        e.preventDefault()
      }
    })

    elButton.addEventListener("click", handler)
  }
}

class HarmonyChat {
  wnd
  ws
  channels
  statusChannel
  currentChannelId
  uid

  constructor() {
    this.uid = null
    this.wnd = new ChatWindow()

    this.statusChannel = {
      name: "𝓼𝓽𝓪𝓽𝓾𝓼",
      chId: "status",
      messages: []
    }

    this.channels = new Map()
    this.resetChannels()

    this.wnd.on("channel:switch", chId => {
      this.showChannel(chId)
    })

    this.wnd.on("chat:send", val => {
      if (val.startsWith("/")) {
        this.handleCommand(val)
      } else {
        if (this.currentChannelId === "status") {
          this.addStatusError("Cannot send messages to pseudo-channels.")
        } else {
          this.handleSendMessage(this.currentChannelId, val)
        }
      }
    })

    this.wnd.on("channel:new", val => {
      this.handleNewChannel(val)
    })

    this.wnd.on("user:invite", val => {
      if (this.currentChannelId === "status") {
        this.addStatusError("Cannot invite others to pseudo-channels.")
      } else {
        this.handleUserInvite(this.currentChannelId, val)
      }
    })

    this.wnd.on("logs:http", val => {
      if (this.uid === null) {
        this.addStatusError("Login or register first.")
        return
      }

      const url = this.currentChannelId === "status" ?
          `/logs/${this.uid}` :
          `/logs/${this.uid}/${this.currentChannelId}`

      const newWindow = window.open(url, "_blank")
      newWindow.focus()
    })

    this.wnd.on("logs:ftp", val => {
      if (this.uid === null) {
        this.addStatusError("Login or register first.")
        return
      }

      const host = document.location.hostname
      const url = this.currentChannelId === "status" ?
          `ftp://${this.uid}@${host}:${FTP_PORT}/` :
          `ftp://${this.uid}@${host}:${FTP_PORT}/${this.currentChannelId}`

      const newWindow = window.open(url, "_blank")
      newWindow.focus()
    })

    this.connect()
  }

  resetChannels() {
    this.channels.clear()
    this.channels.set("status", this.statusChannel)
    this.wnd.setChannelList(this.channels)
    this.showChannel("status")
  }

  joinChannel(name, chId, messages) {
    if (this.channels.has(chId)) {
      return
    }

    this.channels.set(chId, {
      name: name,
      chId: chId,
      messages: messages
    })

    this.wnd.setChannelList(this.channels)
    this.addStatusMessageToChannel(chId, `You've joined channel ${name}!`)
  }

  showChannel(chId) {
    const channel = this.channels.get(chId)
    if (channel) {
      this.wnd.switchToChannel(channel.name, channel.chId, channel.messages)
      this.currentChannelId = chId
    } else {
      console.error(`Missing channel ID "${chId}" (showChannel)`)
    }
  }

  addMessageToChannel(chId, msg) {
    if (msg.text.length === 0) {
      return
    }

    const channel = this.channels.get(chId)
    if (channel) {
      channel.messages.push(msg)

      if (this.currentChannelId === chId) {
        this.wnd.addChatMessage(msg)
      }

    } else {
      console.error(`Missing channel ID "${chId}" (addMessageToChannel)`)
    }
  }

  addStatusMessageToChannel(chId, text) {
    this.addMessageToChannel(chId, {
      type: "server",
      text: text
    })
  }

  addStatusMessage(text) {
    this.addMessageToChannel("status", {
      type: "server",
      text: text
    })
  }

  addStatusError(text) {
    this.addMessageToChannel("status", {
      type: "error",
      text: text
    })
  }

  connect() {
    const ws = new WebSocket(`ws://${document.location.host}/chat`)
    ws.onopen = this.sockOnOpen.bind(this)
    ws.onclose = this.sockOnClose.bind(this)
    ws.onmessage = this.sockOnMessage.bind(this)
    ws.onerror = this.sockOnError.bind(this)
    this.ws = ws
  }

  sendToServer(jsonSerializableData) {
    if (this.ws && this.ws.readyState === 1) {
      this.ws.send(JSON.stringify(jsonSerializableData))
    } else {
      this.addStatusMessage("Failed to send to server (not ready).")
    }
  }

  sockOnOpen() {
    this.addStatusMessage("Connected!")
    this.addStatusMessage(`Either login:
  /login UID
or create a new user:
  /register NameToDisplay`)
  }

  sockOnClose() {
    this.ws = null
    this.uid = null
    this.resetChannels()
    this.addStatusMessage("Disconnected. Reconnecting in 5 seconds.")
    setTimeout(this.connect.bind(this), 5000)
  }

  sockOnMessage(ev) {
    const packet = JSON.parse(ev.data)


    switch (packet.type) {
      case "server":
        this.addStatusMessage(packet.msg)
        break

      case "error":
        this.addStatusError(packet.msg)
        break

      case "joined":
        packet.channels.forEach(channel => {
          this.joinChannel(channel.name, channel.chId, channel.messages)
        })
        this.showChannel(packet.channels[packet.channels.length-1].chId)
        break

      case "message":
        this.addMessageToChannel(packet.chId, packet.msg)
        break

      case "uid":
        this.uid = packet.uid
        break

      default:
        console.error("Unknown or missing type:", packet)
        break
    }
  }

  sockOnError() {
    this.addStatusError("WebSocket error!")
  }

  handleSendMessage(chId, msg) {
    if (msg.length === 0) {
      return
    }

    this.sendToServer({
      type: "message",
      chId: chId,
      msg: msg
    })
  }

  handleCommand(str) {
    const args = str.split(" ").filter(s => s.length)
    const cmd = args.shift().toLowerCase().substring(1)
    const rawArgs = str.substring(/*slash*/1 + cmd.length + /*space*/1)

    switch (cmd) {
      case "login":
        this.sendToServer({
          type: "login",
          uid: args[0]
        })
        break

      case "register":
        this.sendToServer({
          type: "register",
          displayName: rawArgs
        })
        break

      default:
        this.addStatusMessage(`Unknown command "${cmd}".`)
        break
    }
  }

  handleNewChannel(name) {
    name = name.trim()
    this.sendToServer({
      type: "new-channel",
      name: name
    })
  }

  handleUserInvite(chId, uid) {
    uid = uid.trim()
    this.sendToServer({
      type: "invite",
      chId: chId,
      uid: uid
    })
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.chat = new HarmonyChat
})
