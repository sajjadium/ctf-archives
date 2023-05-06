const express = require('express');
const app = express();
const cookieParser = require('cookie-parser');

const nonHonorsItems = [
  { title: 'Sweatshirt', cost: 30, img: '/public/merch/dnu_sweater.png' },
  { title: 'Bottle', cost: 50, img: '/public/merch/dnu_water.png' },
  { title: 'T-Shirt', cost: 10, img: '/public/merch/dnu_shirt.png' },
  { title: 'Wallet', cost: 2, img: '/public/merch/dnu_wallet.png' },
  { title: 'Keys', cost: 5, img: '/public/merch/dnu_keychain.png' },
  {
    title: 'Tax Documents (not for fraud)',
    cost: 0,
    img: '/public/merch/dnu_tax.png',
  },
];

function giveItems(req, res, next) {
  // You should've gotten honors smh
  try {
    JSON.parse(req.cookies['items']);
  } catch (e) {
    res.clearCookie('items');
    res.cookie('items', JSON.stringify(nonHonorsItems), {
      sameSite: 'None',
      secure: true,
    });
  }
  next();
}

app.use(cookieParser());
app.use(
  '/',
  giveItems,
  express.static(__dirname + '/static', { extensions: ['html'] })
);

app.listen(8080);
