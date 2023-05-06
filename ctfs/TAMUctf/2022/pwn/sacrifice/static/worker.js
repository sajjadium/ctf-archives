importScripts("https://cdnjs.cloudflare.com/ajax/libs/js-sha256/0.9.0/sha256.min.js")

function solvePow({prefix, hardness}) {
    let i = 1;
    while (true) {
        const guess = prefix + i.toString();
        const hasher = sha256.create();
        hasher.update(guess);
        const hash = hasher.array();
        const bytes = Math.floor(hardness / 8);
        const bits = hardness % 8;
        if (
            hash.slice(0, bytes).every((b) => b === 0) &&
            hash[bytes] >> (8 - bits) === 0
        ) {
            return guess;
        }
        i += 1;
    }
}

onmessage = e => {
    const pow = e.data;
    const solve = solvePow(pow);
    postMessage({ pow, solve })
};
