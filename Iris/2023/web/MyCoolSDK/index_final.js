const dotenv = require("dotenv");
const express = require("express");
const octokit = require("octokit");
const url = require("url");
const app = express();
const SHA256 = require("crypto-js/sha256");

const port = 1337;

dotenv.config();
const TOKEN = process.env.TOKEN;

const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

var tokens = {};
var identities = {};

function randomStr(len) {
    let res = "";
    for (let i = len; i > 0; i--) {
        res += chars[Math.floor(Math.random() * chars.length)];
    }
    return res;
}

app.get("/", (req, res) => {
    res.send("Empty route for / for k8s");
});

app.get("/gettoken", (req, res) => {
    let tokenCode = randomStr(32);
    let tokenObj = {
        tokenCode: tokenCode,
        identityCode: undefined,
        timeCreated: Math.floor(Date.now() / 1000),
        status: "UNVALIDATED"
    };
    tokens[tokenCode] = tokenObj;
    console.log("/gettoken: " + tokenCode);
    res.send(tokenCode);
});

app.get("/getiden", (req, res) => {
    let q = url.parse(req.url, true).query;
    if (!q.sdktok) {
        res.send("missing sdktok");
        return;
    } else if (!q.repo) {
        res.send("missing repo");
        return;
    } else if (!q.runid) {
        res.send("missing runid");
        return;
    }
    
    let tokenCode = q.sdktok;
    let tokenObj = tokens[tokenCode];
    if (tokenObj == undefined) {
        res.send("token doesn't exist!");
        return;
    }
    
    if (!hasTokenNotExpired(tokenObj)) {
        res.send("token expired!");
        return;
    }
    
    let ownerName = q.repo.toString().split("/")[0];
    let repoName = q.repo.toString().split("/")[1];
    
    let identityCode = randomStr(32);
    let identityObj = {
        identityCode: identityCode,
        tokenCode: q.sdktok.toString(),
        owner: ownerName,
        repo: repoName,
        runId: q.runid.toString(),
        timeCreated: Math.floor(Date.now() / 1000)
    };
    
    identities[identityCode] = identityObj;
    tokens[tokenCode].identity = identityCode;
    console.log("/getiden: " + identityCode);
    res.send(identityCode);
});

app.get("/checkiden", async (req, res) => {
    let q = url.parse(req.url, true).query;
    if (!q.sdktok) {
        res.send("missing sdktok");
        return;
    }
    
    let tokenCode = q.sdktok;
    let tokenObj = tokens[tokenCode];
    if (tokenObj == undefined) {
        res.send("token doesn't exist!");
        return;
    }
    
    if (!hasTokenNotExpired(tokenObj)) {
        res.send("token expired!");
        return;
    }
    
    let identityObj = identities[tokenObj.identity];
    
    var repoIdentity;
    try {
        repoIdentity = await getRepoIdentity(identityObj.owner, identityObj.repo, identityObj.runId);    
    } catch {
        repoIdentity = undefined;
    }

    if (repoIdentity == undefined) {
        res.send("repo identity failed!");
        return;
    }
    
    if (repoIdentity != identityObj.identityCode) {
        res.send(`repo identity failed! found ${repoIdentity} but expected ${identityObj.identityCode}`);
        return;
    }
    
    tokenObj.status = "VALIDATED";
    
    console.log("/checkiden: " + "OK");
    res.send("OK");
});

app.get("/getsdk", (req, res) => {
    let q = url.parse(req.url, true).query;
    if (!q.sdktok) {
        res.send("missing sdktok");
        return;
    }
    
    let tokenCode = q.sdktok;
    let tokenObj = tokens[tokenCode];
    if (tokenObj == undefined) {
        res.send("token doesn't exist!");
        return;
    }
    
    if (!hasTokenNotExpired(tokenObj)) {
        res.send("token expired!");
        return;
    }
    
    if (tokenObj.status == "VALIDATED") {
        tokenObj.status = "EXPIRED";
        res.sendFile("coolsdk.tar.gz", {root: __dirname});
    } else {
        res.send("no u");
    }
});

app.listen(port, () => {
    console.log(`My cool sdk server running on ${port}`);
});

function hasTokenNotExpired(tokenObj) {    
    if (tokenObj.status == "EXPIRED" || (Date.now() / 1000) - tokenObj.timeCreated > 120) {
        tokenObj.status = "EXPIRED";
        return false;
    }
    return true;
}

async function getRepoIdentity(owner, repo, runId) {
    const octo = new octokit.Octokit({
        auth: TOKEN
    });

    let runJobInfo = await octo.request("GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs", {
        owner: owner,
        repo: repo,
        run_id: runId
    });
    
    let jobLogInfo = await octo.request("GET /repos/{owner}/{repo}/actions/jobs/{job_id}/logs", {
        owner: owner,
        repo: repo,
        job_id: runJobInfo.data.jobs[0].id
    });
    
    let logLines = jobLogInfo.data.split(/\r?\n/);
    
    // only check after job begins
    let startPos = 0;
    for (let i = 0; i < logLines.length; i++) {
        if (logLines[i].includes("Job is about to start running on the hosted runner")) {
            startPos = i + 1;
            break;
        }
    }

    // scan for server id string
    let idenStr = undefined;
    const target = "ServerID-";
    for (let i = startPos; i < logLines.length; i++) {
        if (logLines[i].includes(target) && !logLines[i].includes("echo")) {
            let idx = logLines[i].indexOf(target);
            let len = target.length;
            
            idenStr = logLines[i].substring(idx + len);
            break;
        }
        if (logLines[i].includes("##[debug]")) {
            return undefined;
        }
    }

    if (idenStr == undefined) {
        return undefined;
    }

    // verify workflow file
    let runInfo = await octo.request("GET /repos/{owner}/{repo}/actions/runs/{run_id}", {
        owner: owner,
        repo: repo,
        run_id: runId
    });

    let runHeadSha = runInfo.data.head_sha;
    let runFilePath = runInfo.data.path;

    let fileInfo = await octo.request("GET /repos/{owner}/{repo}/contents/{path}{?ref}", {
        owner: owner,
        repo: repo,
        path: runFilePath,
        ref: runHeadSha
    });

    let workflowContents = Buffer.from(fileInfo.data.content, "base64");
    let workflowHash = SHA256(workflowContents.toString()).toString();

    const MATCH_HASH = "8951a3d29206cf24600379fba7efeb7d8fc9181353a958f710a32eb786ae8654";
    if (workflowHash != MATCH_HASH) {
        console.log(`expected ${MATCH_HASH}, found ${workflowHash} hash for workflow!`);
        return undefined;
    }
    
    console.log(idenStr);
    return idenStr;
}