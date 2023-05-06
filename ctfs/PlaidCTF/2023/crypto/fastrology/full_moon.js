const { randomInt, createHash } = require('node:crypto');
const readline = require('node:readline').createInterface({
  input: process.stdin,
  output: process.stdout,
});

const warmup_len = randomInt(64);
for (let i = 0; i < warmup_len; i++) {
    Math.random();
}

const prefix_len = 600;
const alphabet = '☿♀♁♂♃♄♅♆♇';

let output = '';
for (let i = 0; i < prefix_len+128; i++) {
    let index = Math.floor(Math.random() * alphabet.length);
    let rand_max = Math.floor(Math.random() * 4);
    let distortion_len = Math.floor(i/125);
    for (let j = 0; j < distortion_len; j++) {
        index ^= Math.floor(Math.random() * rand_max);
    }
    index = Math.min(index, alphabet.length-1);
    output += alphabet[index];
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
