import * as fs from "fs";
import * as anchor from "@project-serum/anchor";
import { BN } from "bn.js";

import * as api from "./api.js"; 
import { parseAccounts, sendInstructions } from "./util.js";

const idl = JSON.parse(fs.readFileSync("../idl/challenge1.json"));
const accountFile = parseAccounts(fs.readFileSync("../" + api.PLAYERFILE));
const player = accountFile.player;
const accounts = accountFile.challengeOne;
const program = new anchor.Program(idl, accounts.programId.toString(), "fake truthy value");
const baseUrl = accountFile.endpoint.match(/^(https*:\/\/[^\/]+)\/.*/)[1];
const conn = new anchor.web3.Connection(accountFile.endpoint);

// all player code goes here
async function attack() {
}

console.log("running attack code...");
await attack();

console.log("checking win...");
const flag = await api.getFlag(baseUrl, player.publicKey, 1);

if(flag) {
    console.log("win! your flag is:", flag);
}
else {
    console.log("no win");
}
