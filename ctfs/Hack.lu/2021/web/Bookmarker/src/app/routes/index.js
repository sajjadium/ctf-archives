const express = require('express')
const router = express.Router()
const ensureAuthenticated = require('../helper/auth').ensureAuthenticated
const generateHash = require('../helper/shim').generateHash
const escapeStringRegexp = require('escape-string-regexp')
const Links = require('../models/Links')



// adding Flag from env
Links.findOneAndUpdate({
        username: 'admin'
    }, 
    {
        $setOnInsert: {
            title: process.env.FLAG,
            url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            hash: generateHash('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'admin')
        }
    }, 
    {
        upsert: true,
        new: true
    })
    .then(console.log('[+] Flag added'))
    .catch(err => console.log(err))



router.get('/', ensureAuthenticated, async (req, res) => {
        let username = req.session.username
        let {filter} = req.query

        let query = {username}
        if(filter){
            query.title = { $regex: escapeStringRegexp(filter) }  
        }
        let items = await Links.find(query).sort({date: -1})

        if(items.length){
            // update csp
            res.header("Content-Security-Policy", "default-src 'none'; style-src *; font-src *; img-src 'self'; script-src 'unsafe-inline'; connect-src 'self';");
            
            return res.render('index', {
                filter: filter,
                items: items,
                username: username
            })
        }
        else{
            res.render('index', {
                filter: filter,
                items: [],
                username: username
            })
        }
        
})

router.post('/add', ensureAuthenticated, (req, res) => {
    let { title, url  } = req.body
    let username = req.session.username
    if(username === 'admin'){
        req.flash('danger', 'Admin can not add new links.')
    }
    else if(!/^https?:\/\//.test(url)){
        req.flash('danger', 'Not a valid URL.')
    }
    else{
        const newLink = new Links({
            username,
            title,
            url,
            hash: generateHash(url, username)
        })
        newLink.save()
            .catch(() => {
                req.flash('danger', 'Could not save!')
            })
    }
    return res.redirect(301, '/');

    
})

router.get('/delete', ensureAuthenticated, async(req, res) => {
    let { id  } = req.query
    let username = req.session.username
    if(username === 'admin'){
        return res.status(400).json({'error': 'Plz dont delete the flag, thanks :)'})
    }
    // check ownership
    let link = await Links.findOne({_id: id, username: username})
    if(link){
            await link.delete()
            return res.json({'msg': "Deleted successfully."})
    }
    else{
        return res.status(400).json({'error': 'Not found.'})
    }
})

router.get('/l', ensureAuthenticated, async(req, res) => {
    let { url, h  } = req.query
    let username = req.session.username

    // no referrer 
    res.header("Referrer-Policy", "no-referrer")
    // update csp
    res.header("Content-Security-Policy", "default-src 'none'; style-src *; font-src *; img-src 'self'; script-src 'unsafe-inline';");


    if (!url){
        return res.redirect('/')
    }
    else if (!/^https?:\/\//.test(url)){
        return res.render('redirect', {
            url: ''
        })
    }
    else if(generateHash(url, username) !== h){
        return res.render('redirect', {
            url: url
        })
    }
    else{
        return res.redirect(url)
    }
})


module.exports = router


