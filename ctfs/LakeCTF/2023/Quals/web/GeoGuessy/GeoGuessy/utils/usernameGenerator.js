const fs = require('fs');

//crypto strong array choices, from https://stackoverflow.com/a/57954758
let rndItem = a=> a[rnd()*a.length|0];
let rnd = ()=> crypto.getRandomValues(new Uint32Array(1))[0]/2**32;

englishAdj = fs.readFileSync('./utils/english-adjectives.txt', 'utf8').split('\n')
englishNouns = fs.readFileSync('./utils/english-nouns.txt', 'utf8').split('\n')

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function generateUsername() {
    return capitalizeFirstLetter(rndItem(englishAdj)) + capitalizeFirstLetter(rndItem(englishNouns)) + Math.floor(Math.random()*10000)
}

module.exports = generateUsername;