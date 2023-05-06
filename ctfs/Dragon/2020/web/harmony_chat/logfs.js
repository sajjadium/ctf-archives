"use strict"
const fs = require("fs")

const logfs = {}

logfs.ChatLogFS = class ChatLogFS {
  user

  constructor(user) {
    this.user = user
  }

  unlink(path, callback) {
    callback("Error: Read-only FS")
  }

  mkdir(path, optionsOrCallback, callback) {
    callback = callback || optionsOrCallback
    callback("Error: Read-only FS")
  }

  open() {
    throw Error("Should never be used")
  }

  close() {
    throw Error("Should never be used")
  }

  rmdir(path, optionsOrCallback, callback) {
    callback = callback || optionsOrCallback
    callback("Error: Read-only FS")
  }

  rename(oldPath, newPath, callback) {
    callback("Error: Read-only FS")
  }

  createWriteStream(path, options) {
    const fakeWriteStream = new EventEmitter()
    fakeWriteStream.end = () => {}
    setTimeout(() => { fakeWriteStream.emit("error") }, 0)
    return fakeWriteStream
  }

  writeFile(file, data, optionsOrCallback, callback) {
    callback = callback || optionsOrCallback
    callback("Error: Read-only FS")
  }

  createReadStream() {
    throw Error("Should never be used")
  }

  stat(path, optionsOrCallback, callback) {
    callback = callback || optionsOrCallback
    const paths = this.splitPaths(path)

    const s = new fs.Stats()
    const now = new Date()
    s.atime = now
    s.mtime = now
    s.ctime = now
    s.birthtime = now

    if (paths.length === 0) {
      // Return info about root directory.
      s.mode = fs.constants.S_IFDIR | 0o550
      s.size = this.user.channelsPresent.size * 32
    } else if (paths.length === 1) {
      // Info about a specific log.

      const channel = this.user.channelsPresent.get(paths[0])
      if (!channel) {
        callback("Error: File not found")
        return
      }

      s.mode = fs.constants.S_IFREG | 0o440
      s.size = channel.getLogs().length
    } else {
      callback("Error: File not found")
      return
    }

    callback(false, s)
  }

  readFile(path, callback) {
    callback = callback || optionsOrCallback
    const paths = this.splitPaths(path)

    if (paths.length !== 1) {
      callback("Error: File not found")
      return
    }

    const channel = this.user.channelsPresent.get(paths[0])
    if (!channel) {
      callback("Error: File not found")
      return
    }

    callback(false, channel.getLogs())
  }

  readdir(path, callback) {
    callback = callback || optionsOrCallback
    const paths = this.splitPaths(path)

    if (paths.length !== 0) {
      callback("Error: Directory not found")
      return
    }

    callback(false, [...this.user.channelsPresent.keys()])
  }

  splitPaths(path) {
    return path.replace("\\", "/").split("/").filter(p => p.length)
  }
}

module.exports = logfs
