const fastify = require("fastify")({logger: true});
const path = require("path");
const fsp = require("fs/promises");
const crypto = require("crypto");

const pdfbot = require("./pdfbot.js");

const sha256 = (data) => crypto.createHash('sha256').update(data).digest('hex')

fastify.register(require('@fastify/static'), {
    root: path.join(__dirname, 'output'),
});

const queue = [];
fastify.post("/generate", (req, rep) => {
    const { url } = req.body;
  
    if (!url || typeof url !== "string") {
        return rep.send({ success: false, message: "Missing or invalid url" });
    }
  
    try {
        new URL(url);
    } catch (err) {
        return rep.send({ success: false, message: "Invalid url" });
    }
  
    generate(url)
        .then(({ pdf, hash }) => rep.send({ success: true, pdf, hash }))
        .catch((err) => rep.send({ success: false, message: err.message }));
});

const generate = (url) =>
    new Promise((resolve, reject) => {
        queue.push({ url, resolve, reject });
    });

let generating = false;
setInterval(async () => {
    if (generating || queue.length === 0) return;

    const { url, resolve, reject } = queue.shift();
    console.log(`Navigating to: ${url}`);

    try {
        generating = true;
        const pdf = await pdfbot.generate(url);
        generating = false;
        resolve({ pdf, hash: sha256(await fsp.readFile(`./output/${pdf}`)) });
    } catch (err) {
        console.log(err);
        generating = false;
        reject(err);
    }
}, 500);

// cleanup, removes PDFs if more than 5
setInterval(async () => {
    let files = await fsp.readdir("./output/");
    if(files.length <= 5) {
        return;
    }

    files = files.map(async file => (
        { file, stat: await fsp.stat("./output/" + file) }
    ));
    files = await Promise.all(files);
    files = files.sort((a, b) => b.stat.ctimeMs - a.stat.ctimeMs);
    files = files.slice(5).map(f => f.file);

    for(const file of files) {
        await fsp.unlink("./output/" + file);
    }
}, 5000);

fastify.listen({ port: 7778, host: '127.0.0.1' }, () => console.log("pdf-gen internal app listening on port 7778"));