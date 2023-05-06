const express = require('express')
const session = require('express-session')
const cookieParser = require('cookie-parser');
const bot = require('./bot');
const crypto = require('crypto');
const app = express();
const port = 8080;
const FileStore = require('session-file-store')(session);
const bodyParser = require('body-parser');

var FileStoreOptions={logFn: function(){}, reapInterval: 10,}
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies
app.use(cookieParser());
app.use(session({
    name:'session-id',
    secret:`${process.env.SECRET}`,
    saveUninitialized:false,
    resave:false,
    store:new FileStore(FileStoreOptions,),
    cookie: { maxAge: 60000 * 3}
}))

app.set('view engine', 'ejs');
console.log(`${process.env.PASSWORD}`,`${process.env.FLAG}`)

const users = [];

const authenticate = (username, password) =>
{
    for(var i=0; i<users.length; i++)
    {
        if(users[i].username === username)
        {   
             if(users[i].password === password)
             {
                return users[i];
             }
             else
             {
                 return {};
             }
        }
     }
     return {};
}

const find = (username) =>
{
    for(var i=0; i<users.length; i++)
    {
        if(users[i].username === username)
        {
             return true;
        }
    }
    return false;
}

const changeFlag = (username, flag) =>
{
    for(var i=0; i<users.length; i++)
    {
        if(users[i].username === username)
        {
            users[i].flag=flag;
        }
    }
}

const findFlag = (username) =>
{
    for(var i=0; i<users.length; i++)
    {
        if(users[i].username === username)
        {
             return users[i].flag;
        }
    }
    return "";
}

const findFlagByProfile = (profile) =>
{
    for(var i=0; i<users.length; i++)
    {
        if(users[i].profile === profile)
        {
             return users[i].flag;
        }
    }
    return "";
}


const generateProfilePage = () => {
    return crypto.randomBytes(30).toString('hex');
}

const generateRandomFlag = () => {
    return "flag{choose_your_own_flag}";
}

if(!find('admin'))
{
        bot.register(`${process.env.PASSWORD}`);
        console.log(users);
}

app.get('/', (req, res) =>
{
    if(!req.session.user)
    {
        res.redirect('/login');
    }
    else
    {
        res.redirect(`/profile/${req.session.profile}`);
    }
});

app.get('/login', (req, res) =>
{
    if(!req.session.user)
    {
        res.render('login', {message: ''});
    }
    else
    {
        res.redirect(`/profile/${req.session.profile}`);
    }
});

app.get('/register', (req,res) =>
{
    if(!req.session.user)
    {
        res.render('register', {message : '', flag: generateRandomFlag()});
    }
    else
    {
        res.redirect(req.session.profile);
    }
});

app.get('/profile/:profilePage', (req,res) =>
{
    if(!req.session.user)
    {
        res.redirect('/');
    }
    const bytes = crypto.randomBytes(64).toString('hex');
    res.render('profile', {bytes: bytes, flagProfile: findFlagByProfile(req.params.profilePage), flag : findFlag(req.session.user), profile: req.session.profile});
});

app.post('/register', (req, res) =>
{
    const username = req.body.username;
    const password = req.body.password;
    const flag = req.body.flag;
    if(find(username))
    {
        res.render('register', { message : 'User exists', flag: ''} );
    }
    else
    {
        var profile = generateProfilePage();
        users.push({
            username: username,
            password: password,
            profile: profile,
            flag: flag
        });
        req.session.user=username;
        req.session.flag=flag;
        req.session.profile=profile;
        if(username==='admin')
        {
            req.session.cookie.maxAge=365 * 24 * 60 * 60 * 1000;
        }
        res.redirect(`/profile/${profile}`);
    }
});

app.post('/login', (req, res) =>
{
    const username = req.body.username;
    const password = req.body.password;
    user=authenticate(username, password);
    if(Object.keys(user).length>0)
    {
        console.log(user);
        new Promise(resolve => setTimeout(resolve, 5000));
        req.session.user=user.username;
        req.session.flag=user.flag;
        req.session.profile=user.profile;
        res.redirect(`/profile/${user.profile}`);
    }
    else
    {
        res.render('login', { message : 'Incorrect username or password'} );
    }
});

app.get('/logout', (req, res) =>
{
    req.session.destroy((err) =>
    {
        res.clearCookie("session-id");
        res.redirect('/')
    });
});


app.post('/check', (req, res) =>
{
    const flag_user = req.body.flag;
    const flag_admin = users[0].flag;
    if ( flag_user === flag_admin )
    {
        res.render('check', {message: "It matches!", profile: `/profile/${req.session.profile}`});
    }
    else
    {
        res.render('check', {message: "Nope!", profile: `/profile/${req.session.profile}`});
    }
});

app.post('/flag', (req, res) =>
{   
    if(!req.session.user)
    {
        res.redirect('/');
    }
    const flag = req.body.flag;
    changeFlag(req.session.user, flag);
    res.redirect(`/profile/${req.session.profile}`);
});

app.get('/report/:profile', (req, res) =>
{
    bot.visit(
		`http://localhost:${port}/profile/${req.params.profile}`,`${process.env.PASSWORD}`
	);
    res.redirect(`/profile/${req.session.profile}`)
})
app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});