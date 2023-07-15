import fs from "fs";

let config = null;

try {
    console.log("Load config");
    config = JSON.parse(fs.readFileSync("config.json"));
} catch (ex) {
    console.log("Config, not found. Please copy config.json.example to config.json");
    process.exit(1);
}

export default config;