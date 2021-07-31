const fs = require("fs");

// https://www.youtube.com/watch?v=XIhEPwTMjWk

WebAssembly.instantiate(fs.readFileSync(0), {process}).then(({instance}) => {
    instance.exports.main();
});
