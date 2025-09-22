"use strict";

const { createHash, createCipheriv, randomBytes } = require('node:crypto');

const KEY_SIZE_BITS = 256n;
const MAX_INT = 1n << KEY_SIZE_BITS;
const MOD = MAX_INT - 189n; // Prime number
const SEED = MAX_INT / 5n;

function linearRecurrence(seed, exponents) {
    let result = seed;
    let exp = 1n;
    while (exponents > 0n) {
        if (exponents % 2n === 1n) {
            let mult = 1n;
            for (let i = 0; i < exp; i++) {
                result = 3n * result * mult % MOD;
                mult <<= 1n;
            }
        }
        exponents >>= 1n;
        exp++;
    }
    return result;
}
// Generate a random 256 - bit BigInt
function random256BitBigInt() {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    let hex = '0x';
    for (const byte of array) {
        hex += byte.toString(16).padStart(2, '0 ');
    }
    return BigInt(hex);
}
const alicePrivate = random256BitBigInt();
const bobPrivate = random256BitBigInt();
const alicePublic = linearRecurrence(SEED, alicePrivate);
const bobPublic = linearRecurrence(SEED, bobPrivate);
const aliceShared = linearRecurrence(bobPublic,
    alicePrivate);
const bobShared = linearRecurrence(alicePublic, bobPrivate);
console.log("Alice private ", alicePrivate.toString());
console.log("Bob private ", bobPrivate.toString());
console.log("Alice public ", alicePublic.toString());
console.log("Bob public ", bobPublic.toString());
console.log("Alice Shared ", aliceShared.toString());
console.log("Bob Shared ", bobShared.toString());
console.log("Alice's and Bob's shared secrets equal? ",
    aliceShared === bobShared);

function bigIntToFixedBE(n, lenBytes) {
  let hex = n.toString(16);
  if (hex.length % 2) hex = "0" + hex;
  const buf = Buffer.from(hex, "hex");
  if (buf.length > lenBytes) {
    return buf.slice(-lenBytes);
  } else if (buf.length < lenBytes) {
    const pad = Buffer.alloc(lenBytes - buf.length, 0);
    return Buffer.concat([pad, buf]);
  }
  return buf;
}

function sha256(buf) {
  return createHash("sha256").update(buf).digest();
}

function encryptAESGCM(key, plaintext) {
   const iv = randomBytes(12);
   const cipher = createCipheriv('aes-256-gcm', key, iv);
   const ciphertext = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
   const tag = cipher.getAuthTag();
   return { iv, ciphertext, tag };
}

const sharedBytes = bigIntToFixedBE(aliceShared, 32);
const aesKey = sha256(sharedBytes);

const FLAG = "FortID{<REDACTED>}"

const { iv, ciphertext, tag } = encryptAESGCM(aesKey, FLAG);
console.log("ct (hex):   ", Buffer.concat([iv, ciphertext, tag]).toString("hex"));
