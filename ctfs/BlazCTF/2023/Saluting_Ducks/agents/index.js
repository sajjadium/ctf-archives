const { Web3 } = require('web3');
const fs = require('fs');
const express = require('express');
const bodyParser = require('body-parser');

// chain configs
const web3 = new Web3(new Web3.providers.HttpProvider('http://127.0.0.1:8545'));
const PRIVATE_KEY = process.env.PRIVATE_KEY || "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80";
const PUBLIC_KEY = web3.eth.accounts.privateKeyToAccount(PRIVATE_KEY).address;
const DUCK_ADDRESS = process.env.DUCK_ADDRESS || "0xDC11f7E700A4c898AE5CAddB1082cFfa76512aDD";
const DUCK_ABI = JSON.parse(fs.readFileSync('./abi/Ducks.abi', 'utf8'));

// webapp configs
const app = express();
app.use(bodyParser.json());

// store the user token to id mapping and the duck state
let userTokenToId = {};
let userIdToState = {};
const duckMaxLevel = 12;

// send transactions every 5 seconds
let allTxs = [];
async function signTxAndBroadcast(tx) { allTxs.push(tx) }
setInterval(async () => {
    let txs = allTxs;
    allTxs = []; 
    if (txs.length > 0)
        for (let i = 0; i < txs.length; i++) {
            const signedTx = await web3.eth.accounts.signTransaction(txs[i], PRIVATE_KEY);
            try {
                await web3.eth.sendSignedTransaction(signedTx.rawTransaction).on('error', console.error)
            } catch { console.log("Transaction failed") }
        }
}, 5000);

// convert object containing bigints to JSON
function toObject(data) {
    return JSON.parse(JSON.stringify(data, (key, value) =>
        typeof value === 'bigint' ? value.toString() : value
    ));
}

// ABI wrapper
class Abi {
    constructor(functionName) {
        this.functionName = functionName;
        let functionAbi = DUCK_ABI.filter((x) => x.name == functionName)[0]
        this.inputAbi = functionAbi.inputs;
        this.types = [];

        // get the types of the function
        for (let input in functionAbi.inputs) {
            try {
                // get the type of the input, allowing for shorthand
                let ty = functionAbi.inputs[input].type || functionAbi.inputs[input];
                if (!ty) continue;
                // if the type is a tuple, get the components and encode to type
                if (ty.length > 5 && ty.startsWith("tuple")) {
                    let components = functionAbi.inputs[input].components;
                    if (!components || components.length == 0) throw new Error("Tuple components not found")
                    let tupleTypes = components.map((x) => x.type);
                    this.types.push("(" + tupleTypes.join(",") + ")" + ty.slice(5))
                } else {
                    this.types.push(ty);
                }
            } catch {}
        }
        // get the return type of the function
        this.returnType = functionAbi.outputs.map((x) => x.type);
        // get the function signature
        this.signature = functionAbi.name + "(" + this.types.join(",") + ")";
    }

    // utils for encoding 
    getFunctionSignatureHash() { return web3.eth.abi.encodeFunctionSignature(this.signature);}
    encodeParameters(params) { return web3.eth.abi.encodeParameters(this.inputAbi, params) }
    encode(params) { return this.getFunctionSignatureHash() + this.encodeParameters(params).slice(2) }
    
    // utils for calls and sending transactions
    async sendTx(params) {
        return await signTxAndBroadcast({
            from: PUBLIC_KEY,
            to: DUCK_ADDRESS,
            data: this.encode(params),
            value: 0,
            gas: 10000000,
            gasPrice: 10000000000,
        }) 
    }
    async call(params) {
        return web3.eth.abi.decodeParameters(this.returnType, await web3.eth.call({
            from: PUBLIC_KEY,
            to: DUCK_ADDRESS,
            data: this.encode(params),
            value: 0,
            gas: 10000000,
            gasPrice: 10000000000,
        }));
    }
}

// initialize the ABI wrappers for `getDucks`
const getDucks = new Abi("getDucks");


// Wrapper for duck checkpoint
class Checkpoint {
    constructor(userId) {
        this.abi = new Abi("checkpoint");
        this.params = [userId, []];
    }

    initializeAccount(rewardAddr) { this.params[1].push([0, 0, rewardAddr]) }
    mintDuck(timestamp) { this.params[1].push([1, timestamp, 0]) }
    combineDucks(duckLevel) { this.params[1].push([2, 0, duckLevel]) }
    async sendTx() { return await this.abi.sendTx(this.params) }
}

// Emulator for duck checkpoint, checks for timestamp and duck amount
function duckEmulator(_state, actions) {
    // do a deep copy
    let state = JSON.parse(JSON.stringify(_state));
    function avoid(condition, message) { if (condition) throw new Error(message) }
    actions.forEach((action) => {
        const timeNow = Math.floor(Date.now() / 1000);
        avoid(!state.initialized, "Account not initialized")
        if (action.type == "mint") {
            avoid(timeNow < state.checkpoint + 3, "Timestamp not increasing")
            state.checkpoint += 3;
            state.ducks[0].amount += 1;
            state.ducks[0].names = state.ducks[0].names || [];
            state.ducks[0].names.push(action.duckName);
        } else if (action.type == "combine") {
            avoid((action.level < 1 || action.level >= duckMaxLevel), "Invalid level")
            state.ducks[action.level].amount += 1;
            state.ducks[action.level].names = state.ducks[action.level].names || [];
            state.ducks[action.level].names.push((action.duckNames).join("❤️"));
            state.ducks[action.level].lastCombined = action.duckNames[0];

            avoid(state.ducks[action.level - 1].amount < 2, "Not enough ducks")
            state.ducks[action.level - 1].names = state.ducks[action.level - 1].names
                .filter((x) => action.duckNames.indexOf(x) == -1);
            state.ducks[action.level - 1].amount -= 2;
        }
    });
    return state;
}


// static serving for frontend at ./frontend
app.use(express.static('./frontend'))

// API endpoints

// Register a new user
app.get('/register', async (req, res) => {
    const userToken = req.query.userToken;
    const rewardAddr = req.query.rewardAddr;
    if (!userToken || !rewardAddr) return res.send({succuss: false, error: "invalid request"})
    if (userTokenToId[userToken]) return res.send({succuss: false, error: "already registered"})
    // get a random bigint
    const randomBigInt = BigInt(web3.utils.randomHex(32));
    // store the userToken to id mapping
    userTokenToId[userToken] = randomBigInt;
    // initialize the account
    const checkpoint = new Checkpoint(randomBigInt);
    checkpoint.initializeAccount(rewardAddr);
    // send the transaction
    try { await checkpoint.sendTx() } 
    catch (e) { return res.send({succuss: false, error: e}) }
    // initialize the duck state
    let ducks = {}
    for (let i = 0; i < duckMaxLevel; i++) ducks[i] = {amount: 0, names: [], lastCombined: ""}
    userIdToState[randomBigInt] = {initialized: true, checkpoint: new Date().getTime() / 1000 - 5, ducks}
    res.send({succuss: true})
});


// Submit a checkpoint
app.post('/checkpoint', async (req, res) => {
    const data = req.body;
    const { userToken, sequences } = data;
    const userId = userTokenToId[userToken];
    const checkpoint = new Checkpoint(userId);
    try {
        userIdToState[userId] = duckEmulator(userIdToState[userId], sequences);
    } catch (e) { return res.send({succuss: false, error: e}) }
    sequences.forEach((sequence) => {
        sequence.type == "mint" && checkpoint.mintDuck(sequence.timestamp);
        sequence.type == "combine" && checkpoint.combineDucks(sequence.level);
    });
    try { await checkpoint.sendTx();
    } catch (e) { return res.send({ succuss: false, error: e}) }
    res.send({ succuss: true });
});

// Get the ducks of a user
app.get('/getDucks', async (req, res) => {
    let userId = userTokenToId[req.query.userToken];
    if (!userId) return res.send({ succuss: false, error: "not found" })
    res.send({
        succuss: true,
        ducks: toObject(await getDucks.call([userId])),
        duckState: userIdToState[userId],
        userId: userId.toString()
    });
});

app.listen(3000, () => {
    console.log('listening on port 3000');
});
