const { randomBytes } = require("crypto");

const bitLength = (number) => {
  return Math.floor(Math.log2(number)) + 1;
};

const byteLength = (number) => {
  return Math.ceil(bitLength(number) / 8);
};

const toBytes = (number) => {
  const size = number === 0 ? 0 : byteLength(number);
  const bytes = new Uint8Array(size);
  let x = number;
  for (let i = size - 1; i >= 0; i--) {
    const rightByte = x & 0xff;
    bytes[i] = rightByte;
    x = Math.floor(x / 0x100);
  }

  return bytes;
};

module.exports = {
  getGenerator: async () => {
    const ed25519 = await import("@noble/ed25519");
    return ed25519.CURVE.Gx;
  },
  fromHex: (string) => {
    return Uint8Array.from(Buffer.from(string, "hex"));
  },
  toHex: (byte_array) => {
    return Buffer.from(byte_array).toString("hex");
  },
  getPrivateKey: async () => {
    const ed25519 = await import("@noble/ed25519");
    return ed25519.etc.randomBytes(31);
    //return ed25519.utils.randomPrivateKey();
  },
  getSessionKey: (length) => {
    return Uint8Array.from(randomBytes(length));
  },
  xor: (message, key) => {
    let array_result = new Uint8Array(message.length);

    for (i = 0; i < message.length; i++) {
      array_result[i] = message[i] ^ key[i];
    }

    return array_result;
  },
  getPublicKeyFromPrivateKey: async (privKey) => {
    const ed25519 = await import("@noble/ed25519");
    // privKey è una stringa esadecimale
    let priv =
      BigInt("0x" + privKey) %
      (2n ** 252n + 27742317777372353535851937790883648493n);
    let pub = ed25519.ExtendedPoint.BASE.mul(priv);
    return [pub.toAffine().x, pub.toAffine().y];
  },

  verifyToken: async (message, privateKey, token) => {
    const ed25519 = await import("@noble/ed25519");
    try {
      let msg = toBytes(message);

      let private_key_bytes = Uint8Array.from(
        Buffer.from("00" + privateKey, "hex")
      );
      let publicKey = await ed25519.getPublicKeyAsync(private_key_bytes);

      return ed25519.verifyAsync(token, msg, publicKey);
    } catch (error) {
      console.log(error);
    }
    return false;
  },
  genChallenge: () => {
    return Math.floor(Math.random() * 999999999999999);
  },
};
