const { join } = require('path')
const fs = require('fs')
const crypto = require('crypto')

const express = require('express')
const expressLayouts = require('express-ejs-layouts')
const cookieParser = require('cookie-parser')
const fileUpload = require('express-fileupload')

const JWTHelper = require('./JWTHelper')
const config = new (require('./config'))()
const dB = new (require('./database'))()
const authMiddleware = require('./AuthMiddleware')(dB)

const app = express()
const uploads = join(__dirname, 'uploads')
app.use(fileUpload({
    limits: {
	    fileSize: 0.5 * 1024 * 1024 // 0.5 MB
    },
    abortOnLimit: true
}));

const response = (msg, ...details) => ({ message: msg, details });
const isValidFile = (file) => { 
	return [
        'jpg',
		'jpeg',
		'png',
	].includes(file.name.split('.').slice(-1)[0])
}

app.use('/uploads', express.static(uploads))
app.use(express.urlencoded({ extended: false }))
app.use(cookieParser())
app.use(expressLayouts)
app.set('view engine', 'ejs')

app.use((_req, res, next) => { res.locals.user = { uuid: false }; next() })

app.get('/', (_req, res) => {
    try {
        res.render('index', {
            title: 'Home',
            images: dB.admin.images
        })
    } catch (err) {
        res.status(500)
    }
})

app.get('/register', (_req, res) => {
    res.render('form', {
        title: 'Register',
        type: 'Register',
        action: '/register'
    })
})

app.get('/login', (_req, res) => {
    res.render('form', {
        title: 'Login',
        type: 'Login',
        action: '/login'
    })
})

app.get('/gallery', authMiddleware, async (_req, res) => {
    let images, user = res.locals.user
    try {
        images = await dB.getImages(user.uuid)
    } catch (error) {
        res.status(500)
        return
    }
    res.render('gallery', {
        title: 'Gallery',
        flag: user.uuid === dB.admin.uuid ? process.env.FLAG : false,
        images
    })
})

app.get('/.well-known/jwks.json', (_req, res) => {
	return res.json({
		'keys': [
			{
				'alg': 'RS256',
				'kty': 'RSA',
				'use': 'sig',
				'e': 'AQAB',
				'n': config.KEY_COMP.n.toString('base64'),
				'kid': config.KID
			}
		]
	});
});

app.get('/logout', async (req, res) => {
    if (req.cookies.session === undefined) {
        if (!req.is('application/json')) return res.redirect('/');
        return res.status(401).send(response('Authentication required!'));
    }
    let uuid
    try {
        uuid = (await JWTHelper.getPayload(req.cookies.session)).uuid
    } catch (error) {
        res.status(500).send(response("Invalid session token supplied!"))
        return
    }
    if (uuid !== dB.admin.uuid) {
        try {
            const images = await dB.getImages(uuid)
            for (const { fileName } of images) {
                fs.unlinkSync(join(uploads, fileName))
            }
            await dB.Users.destroy({
                where: { uuid }
            })
        } catch (error) {
            console.log(error)
        }        
    }
    res.clearCookie('session');
    res.redirect('/');
});

app.post('/register', async (req, res) => {
    const { username, password } = req.body;

    if (username && password) {
        try {
            await dB.registerUser({
                    username,
                    password
            })
            res.redirect('/login')
        } catch (error) {
            res.status(403).send(response('This username is already registered!'))
        }
        return
    }
    return res.status(401).send(response('Please fill out all the required fields!'));
})

app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    if (username && password) {
        const user = await dB.loginUser(
            username,
            password
        )
        if (!user) {
            res.status(403).send(response('Invalid email or password!'))
            return
        }
        const token = await JWTHelper.sign(
            { uuid: user.uuid }, 
            config.PRIVATE_KEY,
            `${config.AUTH_PROVIDER}/.well-known/jwks.json`, 
            config.KID
        )
        res.cookie('session', token, { maxAge: 43200000 });
        res.redirect('/gallery');
        return
    }
    return res.status(400).send(response('Missing parameters!'));
})

app.post('/uploads', authMiddleware, async (req, res) => {
    const { user } = res.locals
    if ( user.username == dB.admin.username) return res.redirect('/dashboard')
    if (!req.files || !req.files.fileUpload) return res.status(400).send(response('No files were uploaded.'));
    let fileUpload = req.files.fileUpload;
    if (!isValidFile(fileUpload)) return res.status(403).send(response('The file must be an image!'));
    let fileName = (
        `${user.username}-${user.uuid}-${fileUpload.md5}-${crypto.randomBytes(3).toString('hex')}.${fileUpload.name.split('.').slice(-1)[0]}`
    );
    try {
        if (await dB.getImagesCount(user.uuid) > 2) {
            res.status(403).send(response('You can upload only 3 images.'))
            return
        }
    } catch (error) {
        res.status(500).send(response(error.message))
    }
    uploadPath = join(uploads, fileName);
    fileUpload.mv(uploadPath, (err) => {
        if (err) return res.status(500).send(response('Something went wrong!'));
    });
    await user.addImages([
        await dB.Images.create({ fileName })
    ])
    res.redirect('/gallery')
})

dB.init(() => {
    app.listen(3000, () => {
        console.log("Listening on", 3000)
    })
})
