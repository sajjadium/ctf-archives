const express = require('express')
const userRouter = require('./user')
const shopRouter = require('./shop')

const router = express.Router()

router.use('/user', userRouter)
router.use('/shop', shopRouter)

router.get('/', (req, res) => {
    let {message} = req.query
    res.render('index', {message: message})
})



module.exports = router