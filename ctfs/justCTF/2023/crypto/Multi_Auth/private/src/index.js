const crypto = require('crypto');
const readline = require('readline');


function auth(key, msg) {
    msg = Buffer.from(msg, 'base64');
    const nonce = crypto.randomBytes(12);

    const cipher = crypto.createCipheriv('aes-256-gcm', key, nonce);
    cipher.setAAD(msg);
    cipher.final();
    let tag = cipher.getAuthTag();
    return JSON.stringify({"success": true, "signature": Buffer.concat([nonce, tag]).toString('base64')});
}

function verify(key, msg, sig) {
    msg = Buffer.from(msg, 'base64');
    let ivtag = Buffer.from(sig, 'base64');
    let nonce = ivtag.slice(0, 12);
    let tag = ivtag.slice(12);

    const decipher = crypto.createDecipheriv('aes-256-gcm', key, nonce);
    decipher.setAAD(msg)
    decipher.setAuthTag(tag);
    decipher.final();
    return JSON.stringify({"success": true, "signature": ""});
}

function main() {
    console.log("AES authenticator started");

    const key = crypto.generateKeySync('aes', { length: 256 });
    const failure = JSON.stringify({"success": false, "signature": ""})
    const rl = readline.createInterface({
        input: process.stdin, 
        output: process.stdout,
    })

    rl.on('line', (line) => {
        try {
            let rpc = JSON.parse(line);
            if (rpc['message'] === undefined || rpc['message'].length === 0) {
                console.log(failure);
                return;
            }

            if (rpc['method'] === 'auth') {
                console.log(auth(key, rpc['message']));

            } else {
                if (rpc['signatures'] === undefined || rpc['signatures']['aes'] === undefined) {
                    console.log(failure);
                    return;
                }

                console.log(verify(key, rpc['message'], rpc['signatures']['aes']))
            }
        } catch {
            console.log(failure)
        }
    });
}

main();

