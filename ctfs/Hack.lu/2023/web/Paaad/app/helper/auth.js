const ensureAuthenticated = (req, res, next) => {
    if(!req.session.username){
        req.flash('danger', 'You have to login first.')
        res.redirect(`/user/login`)
    }
    else{
        return next()
    }
}

module.exports = {
    ensureAuthenticated,
}