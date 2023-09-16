const ejs = require("ejs");

const { filename, ...query } = JSON.parse(process.argv[2].trim());
ejs.renderFile(filename, query).then(console.log);
