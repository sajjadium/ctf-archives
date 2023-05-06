import { subtle, getRandomValues } from 'crypto'

async function generateX25519Key () {
  return crypto.subtle.generateKey(
    {
      name: 'ECDH',
      namedCurve: 'P-521'
    },
    true,
    ['deriveKey']
  )
}
async function encodeKey (key) {
  return crypto.subtle.exportKey('jwk', key)
}
async function calcSharedSecret (privateKey, publicKey) {
  const aes = {
    name: 'AES-GCM',
    length: 256
  }
  const ec = {
    name: 'ECDH',
    public: publicKey
  }
  const usage = ['encrypt', 'decrypt']

  return crypto.subtle.deriveKey(ec, privateKey, aes, false, usage)
}
async function encryptMessage (plaintext, secret) {
  const ec = new TextEncoder()
  const iv = getRandomValues(new Uint8Array(16))

  const ciphertext = await subtle.encrypt({
    name: 'AES-CBC',
    iv
  }, secret, ec.encode(plaintext))

  return new Uint8Array([...iv, ...ciphertext])
}
async function decryptMessage (ciphertext, secret) {
  const iv = ciphertext.subarray(0, 16)
  const _ciphertext = ciphertext.subarray(16)

  const dec = new TextDecoder()
  const plaintext = await subtle.decrypt({
    name: 'AES-CBC',
    iv
  }, secret, _ciphertext)
  return dec.decode(plaintext)
}

export {
  generateX25519Key,
  encodeKey,
  calcSharedSecret,
  encryptMessage,
  decryptMessage
}
