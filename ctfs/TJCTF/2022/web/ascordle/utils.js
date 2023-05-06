const randStr = (len = 16) => {
  const chars = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_ `abcdefghijklmnopqrstuvwxyz{|}~"
  let rv = ""
  for (let i = 0; i < len; i++) {
      rv += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return rv
}

module.exports = { randStr }
