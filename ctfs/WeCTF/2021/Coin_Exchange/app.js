let path = require('path');
let sha256 = require('sha256')
let http = require('http');
const fileSystem = require("fs");
const WebSocketServer = require('websocket').server
const ReadWriteLock = require('rwlock');
let DB_LOCK = new ReadWriteLock();
const fetch = require('node-fetch');


// serve the index.html file for all routes, nothing wrong here
let server = http.createServer(function(request, response) {
  let filePath = path.join(__dirname, 'index.html');
  let stat = fileSystem.statSync(filePath);
  response.writeHead(200, {'Content-Type': 'text/html', 'Content-Length': stat.size});
  fileSystem.createReadStream(filePath).pipe(response);
});

// declare the http & ws server
server.listen(4000, function() {console.log("Server Started")});
let wsServer = new WebSocketServer({httpServer: server, autoAcceptConnections: false});

// keeps the mapping between token and user data
DB = {};

FLAG = process.env.FLAG ? process.env.FLAG : "we{testflag}"
ADMIN_TOKEN = process.env.ADMIN_TOKEN ? process.env.ADMIN_TOKEN : "admin"

// add admin
DB[ADMIN_TOKEN] = {
  username: "TheBoss",
  base_balance: 1e12,
  trade_history: [],
  is_admin: true
}

// keeps an array of top 10 user having high Total Net USD Value (TNUV)
RANKINGS = [];

usd_to_eth_ratio= 2500
eth_to_usd_ratio= 1/usd_to_eth_ratio
trade_fee = 1

// get eth rate from cryptocompare.com
function get_eth_rate(){
  fetch("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD")
      .then(resp => resp.json())
      .then(r => {
        usd_to_eth_ratio = r.USD;
        eth_to_usd_ratio = 1/r.USD;
      })
}

// get eth rate every 4s
setInterval(get_eth_rate, 4000)

// login API
function login(data) {
  let {username, password} = data;
  let token = sha256(`${username}@${password}`);
  if (!DB[token])
    DB[token] = {
      username: username,
      base_balance: 1000,
      trade_history: [],
      is_admin: false
    };
  return {type: "set_token", content: {token: token}};
}

// ping pong API
function routine(token){
  if (!token || !DB[token]) return {type: "error", content: {}}
  return {
    type: "routine", content: {
      usd_to_eth_ratio: usd_to_eth_ratio,
      eth_to_usd_ratio: eth_to_usd_ratio,
      base_balance: DB[token].base_balance,
      trade_history: DB[token].trade_history,
      rankings: RANKINGS,
      flag: calculate_tnuv(DB[token].base_balance, DB[token].trade_history) > 5000 ? FLAG : "Nothing for you"
    }
  };
}

// helper func for getting usd, eth amount of account based on user trade history
function calculate_usd_eth_amount(base_balance, trade_history){
  let usd = base_balance;
  let eth = 0;
  trade_history.forEach(v => {
    usd += v.amount_in_usd;
    eth += v.amount_in_eth;
  });
  return {usd: usd, eth: eth}
}

// helper func for getting total net usd value = usd + eth * usd/eth
function calculate_tnuv(base_balance, trade_history){
  let {usd, eth} = calculate_usd_eth_amount(base_balance, trade_history)
  return usd + eth * usd_to_eth_ratio
}

// update ranking array
function generate_ranking(){
  RANKINGS = []
  for (const dbKey in DB) {
    let {base_balance, trade_history, username} = DB[dbKey]
    let tnuv = calculate_tnuv(base_balance, trade_history);
    RANKINGS.push({tnuv: tnuv, username: username})
  }
  RANKINGS.sort(function(a,b){return a.tnuv < b.tnuv});
  RANKINGS = RANKINGS.slice(0, 10)
}

// update ranking every sec
setInterval(generate_ranking, 1000);

// buy eth API
function buy(content, token){
  if (!token || !DB[token])
    return {type: "error", content: {}}
  let amount = parseFloat(content["amount"]);
  if (amount < 0) return {type: "message", content: {message: "Nope hacker"}} // dont allow negative trade
  // prevent race condition
  DB_LOCK.writeLock(function (release){
    let {usd} = calculate_usd_eth_amount(DB[token].base_balance, DB[token].trade_history)
    if (amount < usd) DB[token].trade_history.push({amount_in_usd: -amount, amount_in_eth: amount * eth_to_usd_ratio})
    else amount = 0;
    release()
  });
  return {type: "message", content: {message: `Filled ${amount} usd`}};
}

// sell eth API
function sell(content, token){
  if (!token || !DB[token])
    return {type: "error", content: {}}
  let amount = parseFloat(content["amount"]);
  if (amount < 0) return {type: "message", content: {message: "Nope hacker"}}
  // prevent race condition
  DB_LOCK.writeLock(function (release){
    let {eth} = calculate_usd_eth_amount(DB[token].base_balance, DB[token].trade_history)
    if (amount < eth) DB[token].trade_history.push({amount_in_usd: amount * usd_to_eth_ratio, amount_in_eth: -amount})
    else amount = 0;
    release()
  });
  return {type: "message", content: {message: `Filled ${amount} eth`}};
}

// transfer API
function transfer(content, token){
  if (!token || !DB[token]) return {type: "error", content: {}}
  let amount = parseFloat(content["amount"]);
  let to_token = content["to_token"];
  if (!DB[token].is_admin) return {type: "message", content: {message: `Only admin can transfer :(`}};
  if (amount < 0 || amount > 100) return {type: "message", content: {message: `Bad transfer`}};
  DB_LOCK.writeLock(function (release){
    let {eth} = calculate_usd_eth_amount(DB[token].base_balance, DB[token].trade_history)
    if (amount < eth){
      DB[token].trade_history.push({
        amount_in_usd: 0,
        amount_in_eth: 0//-amount
      });
      DB[to_token].trade_history.push({
        amount_in_usd: 0,
        amount_in_eth: amount
      })
    } else amount = 0;
    release()
  });
  return {type: "message", content: {message: `Transferred ${amount} eth`}};
}

// helper function for sending JSON
function sendJson(conn, data){
  conn.sendUTF(JSON.stringify(data));
}

// get the token from the array of cookies
function getToken(cookies){
  for (const cookiesKey in cookies)
    if (cookies[cookiesKey].name === "token") return cookies[cookiesKey].value
}


wsServer.on('request', function(request) {
  try {
    let connection = request.accept('ethexchange-api', request.origin);
    connection.on('message', function(message) {
      if (message.type === 'utf8') {
        try {
          let message_json =  JSON.parse(message.utf8Data);
          switch (message_json["type"]){
            case "init": sendJson(connection, login(message_json["content"])); break;
            case "ping": sendJson(connection, routine(getToken(request.cookies))); break;
            case "buy": sendJson(connection, buy(message_json["content"], getToken(request.cookies))); break;
            case "sell": sendJson(connection, sell(message_json["content"], getToken(request.cookies))); break;
            case "transfer": sendJson(connection, transfer(message_json["content"], getToken(request.cookies)))
          }
        }
        catch (e) {console.log(e)}
      }
    });
    connection.on('close', function(reasonCode, description) {});
  } catch (e) {console.log(e)}

});
