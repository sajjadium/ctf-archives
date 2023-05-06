const bodyParser = require('body-parser')
const ejs = require('ejs')
const express = require('express')
const path = require('path')

const { getProductList, getProductPrice, getProductName } = require('./lib/utils')
const { MONEY, FLAG } = require('./lib/secret')
const { type } = require('os')

const app = express()
const port = 3000

app.engine('.html', ejs.__express)
app.set('view engine', 'html')
app.set('views', path.join(__dirname, 'views'))

app.use(express.static(path.join(__dirname, 'image')))  
app.use(bodyParser.json())

function getMoneyFormat(obj) {
    let tmp = obj.toString()
    let sz = tmp.length
    let res = ""
    for (let i = sz - 1; i >= 0; i -= 3) {
        let x = Math.max(i - 2, 0)
        let part = tmp.substr(x, i - x + 1)
        if (i != sz - 1) part += "."
        res = part + res
    }
    return `Rp${res}`
}

app.locals.moneyfmt = getMoneyFormat

app.get('/', (req, res) => {
    res.render('index', {
        money: MONEY,
        products: getProductList()
    })
})

app.post('/donate', (req, res) => {
    let items = req.body['items']
    let totalItem = 0
    let totalPrice = 0
    let itemResp = []
    try {
        for(item of items) {
            let p = getProductPrice(item.id)
            totalPrice += Math.abs(parseInt(item.quantity * p))
            if (item.id === 4) {
                totalItem += Math.abs(parseInt(item.quantity))
            }
            itemResp.push({
                "name": getProductName(item.id),
                "quantity": item.quantity
            })
        }

        if (totalPrice <= MONEY && 10 <= totalItem && totalItem <= 50) {
            return res.json({
                "status": "success",
                "items": itemResp,
                "totalPrice": getMoneyFormat(totalPrice),
                "message": `Thank you for your donation. Here is your reward: ${FLAG}`
            })
        }

        if (totalPrice > MONEY) {
            return res.json({
                "status": "danger",
                "items": itemResp,
                "totalPrice": getMoneyFormat(totalPrice),
                "message": "Sorry, your money is insufficient"
            })
        }
        if (totalItem < 10 && 50 > totalItem ) {
            return res.json({
                "status": "danger",
                "items": itemResp,
                "totalPrice": getMoneyFormat(totalPrice),
                "message": "Total donation quantity must be between 10 - 50 (inclusive)"
            })
        }

        return res.json({
            "status": "danger",
            "items": itemResp,
            "totalPrice": getMoneyFormat(totalPrice),
            "message": "We are grateful for your intentions, but no reward for you."
        })
    } catch (err) {
        res.status(500)
        return res.json({
            "status": "warning",
            "message": err.message
        })
    }
})

app.listen(port, () => {
    console.log(`Express started on port ${port}`);
})