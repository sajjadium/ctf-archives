import * as fs from "fs";
import got from "got";
import { v4 as uuid } from "uuid";
import { parseAccounts } from "./util.js";

export const PLAYERFILE = "player.json";

const URL = "http://35.188.83.0:3000";

// convenience for making valid rpc requests
// our server interface accepts them, so we must construct them
function rpc(method, params) {
    return {
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            jsonrpc: "2.0",
            id: uuid(),
            method: method,
            params: params,
        }),
    };
}

// create a player. this airdrops 100 sol to a new account and returns its keypair
// the response is formatted as a valid solana keyfile and is saved to disk
export async function createPlayer() {
    const res = (await got.post(`${URL}/player`)).body;

    const obj = parseAccounts(res);

    console.log(`your pubkey is ${obj.player.publicKey.toString()}`);
    console.log(`writing accounts to disk as ${PLAYERFILE}...`);
    fs.writeFileSync("../" + PLAYERFILE, res);

    return obj;
}

// required for building transactions
// we dont provide a full rpc interface so you need to do this yourself
// returns a string, which is in fact the proper typescript type
export async function getLatestBlockhash(url, pubkey) {
    return (await got.post(
        `${url}/${pubkey.toString()}`,
        rpc("getLatestBlockhash", []),
    ).json()).result.value.blockhash;
}

// required for allocating accounts
// i... think this can be calculated offline since its never changed
// but of all the hills i choose this one to be robust on
export async function getMinimumRent(url, pubkey, size) {
    return (await got.post(
        `${url}/${pubkey.toString()}`,
        rpc("getMinimumBalanceForRentExemption", [size]),
    ).json()).result;
}

// posts a signed transaction object to the server
// returns the status code. 200 only means that we made it to chain
// the server does not confirm transactions. it doesnt even handle preflight failure
// the server is not a test environment. please test against your own validator
export async function sendTransaction(url, pubkey, transaction) {
    return (await got.post(
        `${url}/${pubkey.toString()}`,
        rpc("sendTransaction", [transaction.serialize().toString("base64")]),
    ).json()).result;
}

// deploys arbitrary binary data as a solana program. exciting!
// the server pays rent with and assigns authority to a fresh keypair
// technically you can deploy programs yourself via sendTransaction
// but if you actually do that, you should get a hobby
export async function deployProgram(url, pubkey, buffer) {
    return (await got.post(`${url}/program/${pubkey.toString()}`, { body: buffer })).body;
}

// get a flag for a given challenge number
// the way this works is you do whatever transactions you want to achieve a win condition
// then call this, and the server will verify your winstate on chain
export async function getFlag(url, pubkey, challenge) {
    let flag = null;
    try {
        flag = (await got.get(`${url}/flag/${challenge.toString()}/${pubkey.toString()}`)).body;
    }
    catch(e) {}

    return flag;
}
