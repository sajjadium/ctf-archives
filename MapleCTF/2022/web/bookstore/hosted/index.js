import express from 'express'
import bodyParser from 'body-parser'
import session from 'express-session'
import crypto from 'crypto'
import DB from './db.js'
import { validateEmail, validateLogin } from './validator.js';

const PORT = process.env.PORT || 3000

const db = new DB();

let validBooks = await db.getBooks();
validBooks = validBooks.map(book => {
    return {
        id: book.id,
        title: book.title,
        author: book.author,
        price: book.price
    }
});

const app = express();

app.set('view engine', 'ejs');

app.use(session({
    secret: crypto.randomBytes(32).toString('hex'),
    resave: false,
    saveUninitialized: true
}));

app.use(express.static('static'))

app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.render('index');
});

app.get('/login', (req, res) => {
    res.render('login', {
        message: ''
    });
})

app.post('/login', (req, res) => {
    const username = req.body.username;
    const password = req.body.password;

    if (!validateLogin(username, password)) {
        res.render('/login', {
            message: 'Invalid username or password'
        });
    } else {
        db.getUser(username, password, (user) => {
            const userData = {
                username: user.username,
                password: user.password,
                money: 0, // POOR
                books: []
            }
            if (user) {
                req.session.user = userData;
                res.redirect('/books')
            } else {
                res.render('/login', {
                    message: 'User not found'
                });
            }
        });
    }
});

app.get('/register', (req, res) => {
    res.render('register', {
        message: '',
        link: false
    });
})

app.post('/register', (req, res) => {
    const username = req.body.username;
    const password = req.body.password;

    if (!validateLogin(username, password)) {
        res.send('Invalid username or password');
    } else {
        db.register(username, password).then(() => {
            res.render('register', {
                message: 'Registration Successful',
                link: true
            })
        }).catch((err) => {
            res.render('register', {
                message: 'Registration Failed: ' + err,
                link: false
            })
        })
    }
});

app.get('/logout', (req, res) => {
    req.session.destroy();
    res.redirect('/');
});

app.get('/books', (req, res) => {
    if (!req.session.user) {
        res.redirect("/login")
    } else {
        res.render('books', {
            ownedBooks: req.session.user.books,
            books: validBooks
        });
    }
});

app.get('/catalogue', (req, res) => {
    if (!req.session.user) {
        res.redirect('/login');
    } else {
        res.render('catalogue', {
            ownedBooks: req.session.user.books,
            books: validBooks
        });
    }
});

app.post('/purchase', (req, res) => {
    const bookID = req.body?.bookID || '0';
    if (!validBooks.find(book => book.id == bookID)) {
        res.send('Invalid book ID');
    } else {
        const user = req.session.user;
        user.books.push(bookID);
        req.session.user = user;
        res.render('catalogue', {
            ownedBooks: req.session.user.books,
            books: validBooks
        });
    }
    return;
});

app.post('/download-ebook', (req, res) => {
    const option = req.body?.option ?? '';
    const email = req.body?.email ?? '';
    const bookID = req.body?.bookID ?? 1;
    const user = req.session?.user ?? { books: [] };
    if (!validBooks.find(book => book.id == bookID)) {
        res.send('Invalid book ID');
        return;
    } /* else if (!user.books.includes(bookID)) {
        res.send('You do not have this book');
        return;
    } */

    switch (option) {
        case 'direct':
            res.write('Direct downloads currently unavailable. Please wait until the established publish date!');
            break;
        case 'kindle':
            if (validateEmail(email)) {
                db.insertEmail(email, bookID).then((err) => {
                    if (err) {
                        res.send('Error: ' + err);
                    } else {
                        res.send("Email saved! We'll send you a download link once the book has been published!")
                    }
                }).catch((err) => {
                    res.send('Error: ' + err);
                })
            } else {
                res.send("Invalid email address")
            }
            break;
        default:
            res.send('Invalid option');
            break;
    }
});

app.listen(PORT, () => {
    console.log(`listening on port ${PORT}`)
});