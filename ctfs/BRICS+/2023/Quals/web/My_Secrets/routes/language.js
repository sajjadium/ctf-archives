const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    const lang = req.query.lang;

    req.session.lang = lang;
    res.redirect('back');
});

module.exports = router;
