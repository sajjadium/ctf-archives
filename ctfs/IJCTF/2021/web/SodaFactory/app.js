const express = require('express')
const soda = require('sodajs/node');

const app = express()
app.use(express.static('public'))
app.use(express.urlencoded({
  extended: true
}))

var images = {
  coke:"https://kellysdistributors.com.au/wp-content/uploads/387-1.jpg",
  pepsi:"https://static.winc.com.au/pi/70/0f795e8e7cbb8d4c874032865e2c8a246d6416-155505/lgsq.jpg",
  fanta:"https://cdn.shopify.com/s/files/1/2070/6751/products/Fanta.jpg?v=1545098502",
}

app.post('/makeSoda', (req, res) => {
  var {name, brand} = req.body;
  img = images[brand];
  res.send(soda(`
    <title>${name}</title>
    <img src='${img}' alt='${name}'>
  `,{}))
})

app.listen(process.env.PORT,'0.0.0.0', () => {
  console.log(`Listening`)
})
