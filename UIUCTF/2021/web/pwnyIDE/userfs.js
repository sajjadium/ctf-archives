import fs from "fs"
import path from "path"

export default class UserFS {
  constructor(user) {
    this.user = user
  }

  hasPerms(filePath) {
    const relative = path.relative(`/files/${this.user.uid}`, filePath)
    return relative && !relative.startsWith('..') && !path.isAbsolute(relative)
  }

  unlink(_path, callback) {
    callback("Unimplemented")
  }

  open() {
    throw new Error("Unused")
  }

  close() {
    throw new Error("Unused")
  }

  mkdir(_path, optionsOrCallback, callback) {
    callback = callback || optionsOrCallback
    callback("Unimplemented")
  }

  rmdir(_path, optionsOrCallback, callback) {
    callback = callback || optionsOrCallback
    callback("Unimplemented")
  }

  rename(_oldPath, _newPath, callback) {
    callback("Unimplemented")
  }

  writeFile(file, data, optionsOrCallback, callback) {
    const callback2 = callback || optionsOrCallback
    if (!this.hasPerms(file)) {
      callback2("No permission")
      return
    }
    fs.writeFile(file, data, optionsOrCallback, callback)
  }

  stat(path, optionsOrCallback, callback) {
    const callback2 = callback || optionsOrCallback
    if (!this.hasPerms(path)) {
      callback2("No permission")
      return
    }
    fs.stat(path, optionsOrCallback, callback)
  }

  readFile(path, callback) {
    if (!this.hasPerms(path)) {
      callback("No permission")
      return
    }
    fs.readFile(path, callback)
  }

  readdir(path, callback) {
    if (!this.hasPerms(path)) {
      callback("No permission")
      return
    }
    fs.readdir(path, callback)
  }
}

