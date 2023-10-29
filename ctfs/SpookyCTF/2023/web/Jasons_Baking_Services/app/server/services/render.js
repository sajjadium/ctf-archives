exports.homeRoute = (req, res) => {
    res.render('index')
}

exports.registerRoute = (req, res) => {
    res.render('register')
}

exports.dashBoardRoute = (req, res) => {
    username = req.user.name
    res.render('dashboard', { name: username })
}



