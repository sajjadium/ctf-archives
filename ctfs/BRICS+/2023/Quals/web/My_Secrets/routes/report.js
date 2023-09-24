const express = require('express');
const router = express.Router();
const rateLimit = require('express-rate-limit');
const visit = require('../bot')

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 20, // limit each IP to 10 requests per windowMs
  message: 'Too many requests from this IP, please try again later',
  standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers
});

router.get('/', (req, res) => {
    res.render('report', { user: req.session.user, language: req.session.lang });
});

router.post('/',limiter, (req, res) => {
    const reportedLink = req.body.link;
    visit(req.body.link);
    res.send('Link reported successfully!');
});

module.exports = router;
