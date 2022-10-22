var readline = require('readline');
var Crypto = require('vigenere');

var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});

rl.on('line', function(line){
    if (line.length == 20 && line.startsWith("cvctf{") && line.endsWith("}")) {
        var cat = Crypto.encode(line.substring(6, line.length - 1), "nodejsisfun").split('').map(function(c) {
            return String.fromCharCode(c.charCodeAt(0) + 1);
        }).join('');
        if (Buffer.from(cat.split("").reverse().join("")).toString('base64') == "QUlgNGoxT2A2empxMQ==") {
            console.log("Correct!");
        }
    }
});