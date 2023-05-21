const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Gimme something: ', (flag) => {
    const wasmBinBuf = new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 127, 2, 11, 1, 2, 106, 115, 3, 109, 101, 109, 2, 0, 1, 3, 2, 1, 0, 7, 9, 1, 5, 99, 104, 101, 99, 107, 0, 0, 10, 122, 1, 120, 1, 3, 127, 65, 0, 33, 0, 65, 1, 33, 2, 3, 64, 2, 64, 2, 64, 2, 64, 2, 64, 2, 64, 32, 0, 65, 4, 112, 14, 3, 3, 2, 1, 0, 11, 65, 137, 2, 33, 1, 12, 3, 11, 65, 59, 33, 1, 12, 2, 11, 65, 41, 33, 1, 12, 1, 11, 65, 31, 33, 1, 12, 0, 11, 32, 1, 65, 255, 1, 32, 0, 40, 2, 0, 113, 108, 65, 255, 1, 113, 32, 0, 65, 192, 0, 106, 40, 2, 0, 65, 255, 1, 113, 115, 65, 0, 70, 32, 2, 108, 33, 2, 32, 0, 65, 1, 106, 33, 0, 32, 0, 65, 46, 72, 13, 0, 11, 32, 2, 11])
    const wasmMem = new WebAssembly.Memory({ initial: 10, maximum: 100 });
    var strBuf = new TextEncoder().encode(flag.slice(0, 64));
    const memBuf = new Uint8Array(wasmMem.buffer);
    
    for (let i = 0; i < strBuf.length; i++) {
        memBuf[i] = strBuf[i];
    }

    data = [121, 66, 71, 65, 229, 176, 150, 150, 43, 107, 209, 212, 12, 217, 16, 222, 129, 189, 55, 185, 82, 127, 229, 47, 45, 178, 252, 11, 107, 43, 31, 114, 20, 97, 229, 185, 237, 55, 252, 87, 12, 168, 75, 222, 121, 5]

    for (let i = 0; i < data.length; i++) {
        memBuf[i + 64] = data[i] 
    }

    WebAssembly.instantiate(wasmBinBuf, {js: {mem: wasmMem}}).then(wasmModule => {
        result = wasmModule.instance.exports.check();
        if (result) {
            console.log("Correct flag!");
        } else {
            console.log("?")
        }
    });
    rl.close();
});



