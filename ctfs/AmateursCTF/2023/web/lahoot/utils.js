import crypto from "crypto";
// ported from https://stackoverflow.com/a/50066925/10818862
export function secureShuffle(array) {
    const randomNumbers = [];

    for (let i = array.length - 1; i > 0; i--) {
        randomNumbers.push(crypto.randomInt(i));
    }

    // apply durstenfeld shuffle with previously generated random numbers
    for (let i = array.length - 1; i > 0; i--) {
        const j = randomNumbers[array.length - i - 1];
        const temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }

    return array;
}