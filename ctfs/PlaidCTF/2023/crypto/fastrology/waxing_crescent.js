const { randomInt, createHash } = require('node:crypto');
const readline = require('node:readline').createInterface({
  input: process.stdin,
  output: process.stdout,
});

const warmup_len = randomInt(64);
for (let i = 0; i < warmup_len; i++) {
    Math.random();
}

const prefix_len = 135;
const alphabet = '☊☋☌☍';

let output = '';
for (let i = 0; i < prefix_len+128; i++) {
    output += alphabet[Math.floor(Math.random() * alphabet.length)];
}

const prefix = output.substring(0, prefix_len);
const expected = output.substring(prefix_len);

console.log(prefix);
console.log(createHash('md5').update(expected, 'utf8').digest('hex'));

readline.question('❓️\n', guess => {
    readline.close();
    if (guess === expected) {
        console.log('✅');
        process.exit(42);
    } else {
        console.log('❌');
        process.exit(1);
    }
});
