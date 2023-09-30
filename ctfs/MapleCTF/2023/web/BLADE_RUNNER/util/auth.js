function admin(req, res, next) {
    if  (req.session.user) {
        console.log("HERE");
        if (req.session.user != "admin") {
            return res.status(400).send("ADMIN REQUIRED.");
        } else {
            next();
        }
    }else{ 
        return res.status(400).send("LOGIN REQUIRED");
    }
}


module.exports = admin;
