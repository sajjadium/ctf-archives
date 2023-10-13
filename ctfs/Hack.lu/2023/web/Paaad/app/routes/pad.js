const express = require('express')
const router = express.Router()
const ensureAuthenticated = require('../helper/auth').ensureAuthenticated
const Pad = require('../models/Pad')



router.get('/', ensureAuthenticated, async (req, res) => {
     // get id from subdomain
    let id = req.subdomains[0]
    // show the index page
    if(!id){
        let pads = await Pad.find({username: req.session.username})
        return res.render('index', {
            username: req.session.username,
            latest: req.cookies.latest,
            pads
        })
    }
    if (!/^[a-f0-9]{48}$/.test(id)){
        req.flash('danger', 'Invalid päääd id.')
        return res.redirect(`https://${process.env.DOMAIN}`)
    }

    // find pad with id 
    let pad = await Pad.findOne({uniqueId: id})

    if(!pad){
        req.flash('danger', 'Päääd not found.')
        return res.redirect(`https://${process.env.DOMAIN}`)
    }
    // check access
    if(!pad.isPublic && req.session.username != pad.username){
        req.flash('danger', 'Not allowed to access this non-public päääd.')
        return res.redirect(`https://${process.env.DOMAIN}`)
    }


    // edit
    if(req.session.username == pad.username){
        if(req.query.edit=='isPublic'){
            pad.isPublic = !pad.isPublic
            await pad.save()
            return res.redirect(`https://${id}.${process.env.DOMAIN}`)
        }
        if(req.query.edit=='isTemp'){
            pad.createdAt = pad.createdAt ? undefined : new Date()
            await pad.save()
            return res.redirect(`https://${id}.${process.env.DOMAIN}`)
        }
    }

    return res.render('pad', {
        pad: pad
    })
})


router.get('/p/new', ensureAuthenticated, async (req, res) => {
    return res.render('new')
})

router.get('/p/latest', async (req, res) => {
    if(!req.cookies.latest){
        req.flash('danger', 'No latest päääd.')
        return res.redirect('/')
    }
    let id = req.cookies.latest.uniqueId
    if (!/^[a-f0-9]{48}$/.test(id)){
        req.flash('danger', 'Invalid päääd id.')
        return res.redirect(`https://${process.env.DOMAIN}`)
    }
    return res.redirect(`https://${id}.${process.env.DOMAIN}`)
})

router.post('/p/new', ensureAuthenticated, async (req, res) => {
    let {title, content, isPublic, isTemp} = req.body

    let pad = new Pad({
        username: req.session.username,
        title,
        content,
        isPublic: isPublic ? true : false,
        createdAt: isTemp ? new Date() : undefined
    })
    console.log(pad)
    await pad.save()

    res.cookie('latest', {title, uniqueId: pad.uniqueId}, {
        secure: true,
        httpOnly: true,
        sameSite: 'none',
    })
    
    req.flash('success', 'Pad created.')
    return res.redirect('/')    
})





module.exports = router


