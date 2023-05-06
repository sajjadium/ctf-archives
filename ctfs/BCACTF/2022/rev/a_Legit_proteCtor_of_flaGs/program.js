const v0 = process.env.FLAG; // example: bcactf{example flag}

function* v1(v2, v3, v4) {
    while (true) {
        v2 = (v3 * v2 + v4) % 65536
        yield v2;
    }
}

const v5 = ~~(Math.random() * 65536)
const v6 = ~~(Math.random() * 65536)

const v7 = v1(v5, v6, 17483);

const v8 = new TextEncoder().encode(v0);
const v9 = new Uint16Array(v8.buffer);

for (let va = 0; va < v9.length; ++va) {
    v9[va] ^= v7.next().value;
}

let vb = "";

for (const vc of v8) vb += vc.toString(16).padStart(2, "0");

console.log(vb);