const express = require('express')
const app = express()
const port = 80

const bodyParser = require('body-parser')
const morgan = require('morgan')
const path = require('path')

app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json());


app.set('view engine', 'ejs');
app.enable('view cache');

app.use(morgan('combined'));

app.use('/css', express.static(path.join(__dirname, 'node_modules/bootstrap/dist/css')));
app.use('/js', express.static(path.join(__dirname, 'node_modules/bootstrap/dist/js')));
app.use('/js', express.static(path.join(__dirname, 'node_modules/jquery/dist')));
app.use('/img', express.static(path.join(__dirname, 'static/img')));

const products = [{
  name: '1kg of Apples',
  description: 'These juicy, crisp, and delightful apples are handpicked and carefully selected to ensure only the best quality fruits make it to your table. Each apple is bursting with a sweet and refreshing taste that is sure to satisfy your taste buds.',
  price: 'PLN4,99',
  tax: '7%',
  country: 'Poland',
  image: '/img/apple.jpg'
}, {
  name: '1kg of Oranges',
  description: 'Straight from the orchards, these oranges are carefully handpicked at optimal ripeness to ensure maximum flavor and nutrition. Packed with essential vitamins, minerals and antioxidants, these oranges are perfect for adding a healthy pop of color and flavor to your daily diet.',
  price: 'PLN7,99',
  tax: '7%',
  country: 'Poland',
  image: '/img/orange.jpg'
}, {
  name: 'Fishy Fish',
  description: "Introducing \"Fishy Fish\", the ultimate fish-lover's delight! Our fish is sourced from unknown locations, and we cannot guarantee if it is fresh or not. However, we can guarantee that it is packed with flavor and nutrition that will satisfy your cravings. Whether you're a seafood enthusiast or just looking to try something new, \"Fishy Fish\" is the perfect addition to any meal.",
  price: 'PLN99,99',
  tax: '49%',
  country: 'Various',
  image: '/img/fish.jpg'
}, {
  name: '1,000,000 API credits',
  description: "Introducing the <strong>exclusive</strong> 1,000,000 jCTF Social API Request Bundle - the ultimate solution for businesses and individuals who want to maximize their reach on the Orange social network. This bundle includes a massive one million API requests, allowing you to access the full range of features offered by Orange and connect with your target audience with ease.",
  price: '$40,000',
  tax: '23%',
  country: 'Poland',
  image: '/img/server.jpg'
}, {
  name: '2,000,000 API credits',
  description: "Introducing the <strong>exclusive</strong> 2,000,000 jCTF Social API Request Bundle - the ultimate solution for businesses and individuals who want to maximize their reach on the Orange social network. This bundle includes a massive one million API requests, allowing you to access the full range of features offered by Orange and connect with your target audience with ease.",
  price: '$100,000',
  tax: '23%',
  country: 'Poland',
  image: '/img/server.jpg'
}];

app.get('/', (req, res) => {
  return res.render('index', {products});
});

app.post('/', (req, res) => {
  const params = req.body;
  if (typeof params.name !== 'string' ||
      typeof params.description !== 'string' ||
      typeof params.price !== 'string' ||
      typeof params.tax !== 'string' ||
      typeof params.country !== 'string' ||
      typeof params.image !== 'string') {
    res.send('Bad request.');
    return;
  }
  products.push({name: params.name, description: params.description, price: params.price, tax: params.tax, country: params.country, image: params.image});
  return res.render('index', {products});
});

app.all('/product', (req, res) => {
  const params = req.query || {};
  Object.assign(params, req.body || {});

  let name = params.name 
  let strings = params.v;


  if(!(strings instanceof Array) && !Array.isArray(strings)){
    strings = ['NaN', 'NaN', 'NaN', 'NaN', 'NaN'];
  }
  
  // make _0 to point to all strings, copy to prevent reference.
  strings.unshift(Array.from(strings));

  const data = {};
  
  for(const idx in strings){
    data[`_${idx}`] = strings[idx];
  }

  if(typeof name !== 'string'){
    name = `Product: NaN`; 
  }else{
    name = `Product: ${name}`;
  }

  data['productname'] = name;

  data['print'] = !!params.print;


  res.render('product', data);
});


app.listen(port, async () => {
  const testStr = `test4444`;
  const res = await fetch(`http://localhost:${port}/product?name=${testStr}`).then(e=>e.text());
  if(res.includes(testStr)){
    console.log(`App listening on port ${port}`);
  }else{
    throw new Error("Something went wrong while spawning the challenge");
  }
});
