const express = require('express')
const payments = require('./payments')
const pdf = require('./pdf')
const app = express()
const port = 5000
const { v4: uuidv4 } = require('uuid');
const { readFile } = require('fs/promises')
const path = require('node:path');
const cookieParser = require('cookie-parser')

var invoice = null

app.use(express.urlencoded({extended: true}));
app.use(express.static('static'))
app.use(cookieParser())

app.get('/', (req, res) => {
  res.sendFile('index.html', { root: path.join(__dirname, 'templates')})
})

app.get('/cart', (req, res) => {
    res.sendFile('cart.html', { root: path.join(__dirname, 'templates')})
})

app.post('/checkout', async (req, res) => {
  let discountRate = payments.validateDiscount(req.body.discount)
  let id = uuidv4();
  
  //TODO: add support for more products
  let total = 414

  if (total * (1 - discountRate)> 0) {
    try {
      return res.redirect(payments.getPaymentURL(id))
    } catch (e) {
      res.statusCode = 500
      return res.send(e.message)
    }
  }
  
  //TODO: add order to database
  let pdffile = await pdf.renderPdf(req.body)
  res.setHeader('Content-Type', 'application/pdf');
  res.setHeader('Content-Disposition', 'inline; filename=invoice.pdf')
  return res.send(pdffile)
})  

app.get('/renderInvoice', async (req, res) => {
  if (!invoice) {
    invoice = await readFile('templates/invoice.html', 'utf8')
  }

  let html = invoice
  .replaceAll("{{ name }}", req.query.name)
  .replaceAll("{{ address }}", req.query.address)
  .replaceAll("{{ phone }}", req.query.phone)
  .replaceAll("{{ email }}", req.query.email)
  .replaceAll("{{ discount }}", req.query.discount)
  res.setHeader("Content-Type", "text/html")
  res.setHeader("Content-Security-Policy", "default-src 'unsafe-inline' maxcdn.bootstrapcdn.com; object-src 'none'; script-src 'none'; img-src 'self' dummyimage.com;")
  res.send(html)
})

app.get('/orders', (req, res) => {
  if (req.socket.remoteAddress != "::ffff:127.0.0.1") {
    return res.send("Nice try")
  }
  if (req.cookies['bot']) {
    return res.send("Nice try")
  }
  res.setHeader('X-Frame-Options', 'none');
  res.send(process.env.FLAG || 'kalmar{test_flag}')
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
