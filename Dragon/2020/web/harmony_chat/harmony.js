"use strict"
const utils = require("./utils")

const harmony = {}

harmony.User = class User {
  id
  displayName
  channelsOwned
  channelsPresent
  ws

  constructor(displayName) {
    this.id = utils.generateNewId()
    this.displayName = displayName
    this.channelsOwned = new Map()
    this.channelsPresent = new Map()
    this.ws = null
  }

  sendTo(jsonSerializableData) {
    if (this.ws && this.ws.readyState === 1) {
      this.ws.send(JSON.stringify(jsonSerializableData))
    }
  }

  sendToRaw(packet) {
    if (this.ws && this.ws.readyState === 1) {
      this.ws.send(packet)
    }  }

  sendAllChannels() {
    const channels = []
    this.channelsPresent.forEach(channel => {
      channels.push({
        name: channel.name,
        chId: channel.id,
        messages: channel.messages
      })
    })

    this.sendTo({
      type: "joined",
      channels: channels
    })
  }

  sendUserId() {
    this.sendTo({
      type: "uid",
      uid: this.id
    })
  }
}

harmony.Channel = class Channel {
  id
  name
  owner
  present
  messages

  constructor(name, owner) {
    this.id = utils.generateNewId()
    this.name = name
    this.owner = owner
    this.present = new Map()
    this.messages = []

    owner.channelsOwned.set(this.id, this)

    // Auto-join owner.
    this.joinUser(owner)
  }

  joinUser(user) {
    this.present.set(user.id, user)
    user.channelsPresent.set(this.id, this)

    user.sendTo({
      type: "joined",
      channels: [
        {
          name: this.name,
          chId: this.id,
          messages: this.messages
        }
      ]
    })
  }

  getLogs() {
    const lines = []
    this.messages.forEach(msg => {
      if (msg.text !== "") {
        lines.push(`${msg.name}: ${msg.text}`)
      } else {
        lines.push("")
      }
    })

    return lines.join("\r\n")
  }

  postMessage(author, text) {
    if (!this.present.has(author.id)) {
      return
    }

    const parts = []
    let textLength = text.length
    while (textLength >= 0) {
      parts.push(text.substring(0, 512))
      text = text.substring(512)
      textLength -= 512
    }

    const nowUTC = (new Date()).toUTCString()

    parts.forEach(textPart => {
      const msg = {
        name: author.displayName,
        text: textPart.substring(0, 512),
        date: nowUTC
      }

      this.messages.push(msg)
      while (this.messages.length > 100) {
        this.messages.shift()
      }

      const packet = JSON.stringify({
        type: "message",
        chId: this.id,
        msg: msg
      })

      this.present.forEach(user => user.sendToRaw(packet))
    })
  }
}

module.exports = harmony
