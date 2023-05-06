"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var Puppeteer = require("puppeteer");
var Redis = require("ioredis");
var Url = require("url");
var redis = new Redis(6379, "redis");
(function () { return __awaiter(void 0, void 0, void 0, function () {
    var _a, error, data;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                if (!true) return [3 /*break*/, 5];
                return [4 /*yield*/, redis.blpop("query", 0)];
            case 1:
                _a = _b.sent(), error = _a[0], data = _a[1];
                if (!(data && data.startsWith("/") && Url.parse("http://web" + data).host === "web")) return [3 /*break*/, 3];
                console.log("> Start to process - http://web" + data);
                return [4 /*yield*/, (function (url) { return __awaiter(void 0, void 0, void 0, function () {
                        var bot, page;
                        return __generator(this, function (_a) {
                            switch (_a.label) {
                                case 0: return [4 /*yield*/, Puppeteer.launch({
                                        product: "chrome",
                                        headless: true,
                                        ignoreHTTPSErrors: true,
                                        args: ["--no-sandbox"]
                                    })];
                                case 1:
                                    bot = _a.sent();
                                    return [4 /*yield*/, bot.newPage()];
                                case 2:
                                    page = _a.sent();
                                    return [4 /*yield*/, page.setCookie({
                                            domain: "web",
                                            name: "FLAG",
                                            value: process.env.FLAG
                                        })];
                                case 3:
                                    _a.sent();
                                    return [4 /*yield*/, page.goto(url, {
                                            timeout: 10000
                                        }).catch(function (error) {
                                            console.error(error);
                                        })];
                                case 4:
                                    _a.sent();
                                    return [4 /*yield*/, page.close()];
                                case 5:
                                    _a.sent();
                                    return [4 /*yield*/, bot.close()];
                                case 6:
                                    _a.sent();
                                    return [2 /*return*/];
                            }
                        });
                    }); })("http://web" + data)];
            case 2:
                _b.sent();
                console.log("> Job Done.");
                return [3 /*break*/, 4];
            case 3:
                console.error("> Invalid path.");
                _b.label = 4;
            case 4: return [3 /*break*/, 0];
            case 5: return [2 /*return*/];
        }
    });
}); })();
//# sourceMappingURL=app.js.map