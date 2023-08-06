const express = require('express');
const authenticationMiddleware = require('../middleware/authenticationMiddleware');

const { doReportHandler } = require('../util/report');

let db;

const router = express.Router();

router.get('/', (req, res) => {
    if (req.session.userId) {
        
        return res.render('authenticated');
    }
    return res.render('index');
});

router.get('/login', (req, res) => {
    return res.render('login');
});

router.post('/login', async (req, res) => {
    const username = req.body.username;
    const password = req.body.password;

    if (!username || !password) {
        return res.status(400).json({ error: 'Missing username or password' });
    }

    const result = await db.loginUser(username, password);
    if (result) {
        req.session.userId = result.id;
        return res.status(200).json({ success: 'User logged in' });
    } else {
        return res.status(400).json({ error: 'Invalid username or password' });
    }
});

router.get('/register', (req, res) => {
    return res.render('register');
});

router.post('/register', async (req, res) => {
    // console.log(req.body)
    const username = req.body.username;
    const password = req.body.password;

    if (!username || !password) {
        return res.status(400).json({
            error: 'Missing username or password'
        });
    }

    if (password.length < 8) {
        return res.status(400).json({
            error: 'Password must be at least 8 characters long'
        });
    }

    if (await db.userExists(username)) {
        return res.status(400).json({ error: 'User already exists' });
    } else {
        await db.registerUser(username, password);
        return res.status(200).json({ success: 'User registered' });
    }

});

router.post('/create-profile',authenticationMiddleware, async (req, res) => {
    if (!req.session.userId) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    if (!req.body.first_name || !req.body.last_name || !req.body.profile_picture_link) {
        return res.status(400).json({ error: 'Missing infos' });
    }
    try {
        const result = db.createProfile(req.session.userId, req.body.first_name, req.body.last_name, req.body.profile_picture_link, true);
        return res.status(200).json({ decrypted: result });
    } catch (e) {
        return res.status(400).json({ error: 'Invalid request or server error' });
    }
});

router.patch("/make-public",authenticationMiddleware, async (req, res) => {
    if (!req.session.userId ) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    if (!req.body.is_public) {
        return res.status(400).json({ error: 'Missing infos' });
    }

    try {
        await db.makePublic(req.session.userId, req.body.is_public);
        return res.status(200).json({ message: "success" });
    } catch (e) {
        return res.status(500).json({ error: 'Error occurred' });
    }
})


router.get("/my-profile",authenticationMiddleware, async (req, res) => {
    if (!req.session.userId) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    try {
        if (req.session.userId) {
            const result = await db.getProfile(req.session.userId);
            console.log(result)
            if (result.length !== 0) {
                return res.render("my-profile", { profile: result[0] })
            }
            return res.render('create-profile');
        } else {
            return res.redirect('/login');
        }
    }
    catch (e) {

        return res.render("error");
    }
})

router.get("/profile/:id", authenticationMiddleware, async (req, res) => {
    if (!req.session.userId|| req.session.userId !== 1) {
        return res.render("not-authorized");
    }

    const result = await db.getProfile(req.params.id);
    if (result.length === 0) {
        return res.render("404");
    }
    return res.render("my-profile",{profile:result[0]});


    
})

router.get("/search-profile",authenticationMiddleware, async (req, res) => {
    // Not implemented yet only admin can search for now for development purposes
    if (req.session.userId === 1&& req.query['search']) {
        console.log("query"+req.query.search)
        try {
                const result = await db.searchProfile(req.query['search']);
                
                if (result.length !== 0)
                    return res.json({ profiles: result.map(r => r.user_id) });
            else 
                return res.status(404).json({ error: 'No profiles found' })
        }
        catch (e) {
            return res.status(500).json({ error: 'Error occurred' })
        }
    }
    return res.status(500).json({ error: 'idk' })
})


// Report any suspicious activity to the admin!
router.post('/report', doReportHandler);
router.get('/report',authenticationMiddleware, (req, res) => {
    return res.render("report")
});

module.exports = (database, session) => {
    db = database;
    sessionParser = session;
    return router;
};