const express    = require('express')
const bodyParser = require('body-parser')
const mysql      = require(`mysql-await`)
const session    = require('express-session')
const cookieParser = require("cookie-parser")

const pool = mysql.createPool({
  connectionLimit: 50,
  host     : 'localhost',
  user     : '***REDACTED***',
  password : '***REDACTED***',
  database : '***REDACTED***'
})

const app = express()
app.set('strict routing', true)
app.set('view engine', 'ejs')

const rawBody = function (req, res, buf, encoding) {
  if (buf && buf.length) {
    req.rawBody = buf.toString(encoding || 'utf8')
  }
}

app.use(bodyParser.json({verify: rawBody}))
app.use(cookieParser())

app.use(session({
  secret: '***REDACTED***',
  resave: false,
  saveUninitialized: false,
  proxy: true,
  cookie: {
    sameSite: 'none',
    secure: true
  }
}))

app.use(function (req, res, next) {
  if(req.cookies.lang && typeof(req.cookies.lang) == "string")
    req.session.lang = req.cookies.lang


  if(req.query.lang && typeof(req.query.lang) == "string") {
    res.cookie('lang', req.query.lang)
    req.session.lang = req.query.lang
  }

  if(!req.session.lang) 
    req.session.lang = "en"
  next()
});

app.get('/', (req, res) => {
  if(req.session.userid)
    return res.redirect('/wallet')
  res.render('index', {lang: req.session.lang})
})

app.get('/login', (req, res) => {
  if(req.session.userid)
    return res.redirect('/wallet')
  res.render('login', {lang: req.session.lang})
})

app.post('/login', async (req, res) => {
  if(!req.body.login || !req.body.password || (typeof(req.body.login) != "string") || (typeof(req.body.password) != "string") || (req.body.password.length < 8))
    return res.json({success: false})
  const db = await pool.awaitGetConnection()
  try {
    result = await db.awaitQuery("SELECT `id` FROM `users` WHERE `login` = ? AND `password` = ? LIMIT 1", [req.body.login, req.body.password])
    req.session.userid = result[0].id
    res.json({success: true})
  } catch {
    res.json({success: false})
  } finally {
    db.release()
  }
})

app.get('/signup', (req, res) => {
  if(req.session.userid)
    return res.redirect('/wallet')
  res.render('signup', {lang: req.session.lang})
})

app.post('/signup', async (req, res) => {
  if(!req.body.login || !req.body.password || (typeof(req.body.login) != "string") || (typeof(req.body.password) != "string") || (req.body.password.length < 8))
    return res.json({success: false})

  const db = await pool.awaitGetConnection()
  try {
    result = await db.awaitQuery("SELECT `id` FROM `users` WHERE `login` = ?", [req.body.login])
    if (result.length != 0) 
      return res.json({success: false})
    result = await db.awaitQuery("INSERT INTO `users` (`login`, `password`) VALUES (?, ?)", [req.body.login, req.body.password])
    req.session.userid = result.insertId
    db.awaitQuery("INSERT INTO `wallets` (`id`, `title`, `balance`, `user_id`) VALUES (?, 'Default Wallet', 100, ?)", [`0x${[...Array(32)].map(i=>(~~(Math.random()*16)).toString(16)).join('')}`, result.insertId])
    return res.json({success: true})
  } catch {
    return res.json({success: false})
  } finally {
    db.release()
  }
})

app.get('/wallet', async (req, res) => {
  if(!req.session.userid)
    return res.redirect('/')
  const db = await pool.awaitGetConnection()
  wallets = await db.awaitQuery("SELECT * FROM `wallets` WHERE `user_id` = ?", [req.session.userid])
  result = await db.awaitQuery("SELECT SUM(`balance`) AS `sum` FROM `wallets` WHERE `user_id` = ?", [req.session.userid])
  db.release()
  res.render('wallet', {wallets, sum: result[0].sum, lang: req.session.lang})
})

app.post('/transfer', async (req, res) => {
  if(!req.session.userid || !req.body.from_wallet || !req.body.to_wallet || (req.body.from_wallet == req.body.to_wallet) || !req.body.amount 
    || (typeof(req.body.from_wallet) != "string") || (typeof(req.body.to_wallet) != "string") || (typeof(req.body.amount) != "number") || (req.body.amount <= 0))
    return res.json({success: false})

  const db = await pool.awaitGetConnection()
  try {
    await db.awaitBeginTransaction()

    from_wallet = await db.awaitQuery("SELECT `balance` FROM `wallets` WHERE `id` = ? AND `user_id` = ? FOR UPDATE", [req.body.from_wallet, req.session.userid])
    to_wallet = await db.awaitQuery("SELECT `balance` FROM `wallets` WHERE `id` = ? AND `user_id` = ? FOR UPDATE", [req.body.to_wallet, req.session.userid])
    if (from_wallet.length == 0 || to_wallet.length == 0) 
      return res.json({success: false})
    from_balance = from_wallet[0].balance

    if(from_balance >= req.body.amount) {
      transaction = await db.awaitQuery("INSERT INTO `transactions` (`transaction`) VALUES (?)", [req.rawBody])
      await db.awaitQuery("UPDATE `wallets`, `transactions` SET `balance` = `balance` - `transaction`->>'$.amount' WHERE `wallets`.`id` = `transaction`->>'$.from_wallet' AND `transactions`.`id` = ?", [transaction.insertId])
      await db.awaitQuery("UPDATE `wallets`, `transactions` SET `balance` = `balance` + `transaction`->>'$.amount' WHERE `wallets`.`id` = `transaction`->>'$.to_wallet' AND `transactions`.`id` = ?", [transaction.insertId])
      await db.awaitCommit()
      res.json({success: true})
    } else {
      await db.awaitRollback()
      res.json({success: false})
    }
  } catch {
    await db.awaitRollback()
    res.json({success: false})
  } finally {
    db.release()
  }
})

app.post('/wallet', async (req, res) => {
  if(!req.session.userid || !req.body.wallet || (typeof(req.body.wallet) != "string"))
    return res.json({success: false})

  const db = await pool.awaitGetConnection()
  try {
    db.awaitQuery("INSERT INTO `wallets` (`id`, `title`, `balance`, `user_id`) VALUES (?, ?, 0, ?)", [`0x${[...Array(32)].map(i=>(~~(Math.random()*16)).toString(16)).join('')}`, req.body.wallet, req.session.userid])
    res.json({success: true})
  } catch {
    res.json({success: false})
  } finally {
    db.release()
  }
})

app.post('/withdraw', async (req, res) => {
  if(!req.session.userid || !req.body.wallet || (typeof(req.body.wallet) != "string"))
    return res.json({success: false})

  const db = await pool.awaitGetConnection()
  try {
    result = await db.awaitQuery("SELECT `balance` FROM `wallets` WHERE `id` = ? AND `user_id` = ?", [req.body.wallet, req.session.userid])
    /* only developers can have a negative balance */
    if((result[0].balance > 150) || (result[0].balance < 0))
      res.json({success: true, money: FLAG})
    else
      res.json({success: false})
  } catch {
    res.json({success: false})
  } finally {
    db.release()
  }
})

app.get('/logout', (req, res) => {
  req.session.destroy()
  res.redirect('/')
})

const PORT = 8080
const FLAG = "VolgaCTF{***REDACTED***}"

app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`)
})