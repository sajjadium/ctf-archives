"use strict";
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const path = __importStar(require("path"));
const express_1 = __importDefault(require("express"));
const express_http_proxy_1 = __importDefault(require("express-http-proxy"));
exports.main = () => {
    const app = express_1.default();
    app.get("/", async (req, res) => {
        res.sendFile(path.join(__dirname, "client/index.html"));
    });
    app.get("/dist/main.js", async (req, res) => {
        res.sendFile(path.join(__dirname, "client/dist/main.js"));
    });
    app.use("/api/", express_http_proxy_1.default("api:4101"));
    app.listen(8080);
};
exports.main();
