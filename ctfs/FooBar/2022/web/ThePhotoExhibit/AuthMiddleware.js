const JWTHelper = require('./JWTHelper');

const response = data => ({ message: data });

module.exports = dB => async (req, res, next) => {
    try {
        if (req.cookies.session === undefined) {
            if (!req.is('application/json')) return res.redirect('/');
            return res.status(401).send(response('Authentication required!'));
        }
        let header
        try {
            header = await JWTHelper.getHeader(req.cookies.session)
        } catch (error) {
            res.status(500).send(response("Invalid session token supplied!"))
            return
        }
        if (!header.jku || !header.kid){
            res.status(500).send(response('Missing required claims in JWT!'));
            return
        }
        if (header.jku.lastIndexOf('http://localhost:3000', 0) !== 0) {
            res.status(500)
            return
        }
        let pubkey
        try {
            pubkey = await JWTHelper.getPublicKey(header.jku, header.kid)
        } catch (error) {
            console.log(error)
            res.redirect('/logout')
            return
        }
        let data
        try {
            data = await JWTHelper.verify(req.cookies.session, pubkey)
        } catch (error) {
            console.log(data, error)
            res.status(403).send(response('Authentication token could not be verified!'))
            return
        }
        if (!data.uuid) {
            res.status(404)
            return
        }
        let user
        try {
            user = await dB.getUser(data.uuid)
        } catch (error) {
            res.status(500)
            return
        }
        if (user === null) {
            res.status(404)
            return
        }
        res.locals.user = user
        next();
    } catch (error) {
        res.status(500).send(response(error.toString()));
    }
}
