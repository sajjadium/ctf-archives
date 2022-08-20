import { Keypair, PublicKey } from "@solana/web3.js";
import * as api from "./api.js"; 
import { Transaction } from "@solana/web3.js";

// dont leave home without it
export function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// convenience for converting all pubkeys and keypairs
export function parseAccounts(o) {
    return _parseAccounts(
        typeof o === "string"
        || o instanceof Buffer
        ? JSON.parse(o)
        : JSON.parse(JSON.stringify(o))
    );
}

function _parseAccounts(o) {
    if(typeof o === "string") {
        try {
            o = new PublicKey(o);
        } catch(e) {}
        return o;
    }
    else if(o instanceof Array) {
        return Keypair.fromSecretKey(Buffer.from(o));
    }
    else {
        for (var [k, v] of Object.entries(o)) {
            o[k] = _parseAccounts(v);
        }
        return o;
    }
}

// convenience to wrap and send instructions
// takes list of instructions, list of signer keypairs, and optional player pubkey
// in most (all?) cases the first signer will be the player, so
export async function sendInstructions(url, ixns, signers, player = signers[0].publicKey) {
    let txn = new Transaction();
    for (let ixn of ixns) {
        txn.add(ixn);
    }

    txn.recentBlockhash = await api.getLatestBlockhash(url, player);
    txn.sign(...signers);

    return await api.sendTransaction(url, player, txn);
}
