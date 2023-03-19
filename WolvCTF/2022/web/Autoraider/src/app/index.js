const express = require('express');
const session = require('express-session');

const multer = require('multer');
const bodyParser = require('body-parser');
const upload = multer();

const redis = require('redis');

const {VM} = require('vm2');

const SESSION_SECRET = process.env.REDIS_SECRET || 'secret';
const FLAG = process.env.FLAG || 'wsc{dummy}';

const NUM_QUESTIONS = 30;

var app = express()

let sessionOptions = {
    secret: SESSION_SECRET,
    resave: false,
    saveUninitialized: true
}

// ------ For running the challenge in Google Cloud with Redis session storage -----
// Ignore this if running locally
if(process.env.REDIS_IP) {
    var RedisStore = require('connect-redis')(session)
    const client = redis.createClient({
      "host": process.env.REDIS_IP
    });
    client.on('connect', () => console.log('Connected to Redis!'));
    client.on("error", (error) => console.error('Redis Error: ', error));
    sessionOptions['store'] = new RedisStore({ client: client });
}
// ----------------------------------------------------------------------------------

app.use(session(sessionOptions));

// Make sure correct answers always exist in session
app.use((req, res, next) => {
    if(!req.session.answers) {
        req.session.answers = generateAnswers();
    }
    next();
});

app.use(express.static('public'));

// for parsing application/json
app.use(bodyParser.json()); 

// for parsing application/xwww-
app.use(bodyParser.urlencoded({ extended: true })); 
//form-urlencoded

// for parsing multipart/form-data
app.use(upload.array()); 

app.post('/upload', async (req, res, next) => {
    try {
        let code = req.body.code;

        const vm = new VM({
            timeout: 50,
            allowAsync: false
        });
        
        // Test for correct responses for given person
        // Correct answers retrieved from user session
        const person = req.session.answers.person;
        const responses = req.session.answers.responses;
        let testCases = responses.map((response, i) => { 
            return {'person': person, 'questionNumber': i, 'correct': response}
        });
        // Add edge case
        testCases.push(
            {'person': 9999999999, 'questionNumber': 0, 'correct': false}
        )

        // Go through each test case
        for(i in testCases) {
            const testCase = testCases[i];
            const result = testCode(vm, code, testCase.person, testCase.questionNumber, testCase.correct);
            if(result.error) {
                req.session.pass = false;
                res.send(result.message);
                return;
            } else if(!result.pass) {
                req.session.pass = false;
                res.redirect('submission.html');
                return;
            }
        };
        
        req.session.pass = true;
        res.redirect('submission.html');
    } catch {
        res.send('Server side error');
    }
});

app.get('/grade', async (req, res, next) => {
    if(req.session.pass || false) {
        res.send('Tests passed! Here is the flag: ' + FLAG);
    } else {
        req.session.answers = generateAnswers();
        res.send('Tests failed. Correct answers have been changed!');
    }
});

function generateAnswers() {
    answers = {
        'person': Math.floor(Math.random() * 7753000), // Random person in the world
        'responses': []
    };
    for(let i = 0; i < NUM_QUESTIONS; i++) {
        answers.responses.push(Math.random() > 0.5);
    }
    return answers;
}

function testCode(vm, code, person, questionNumber, correct) {
    ret = {
        message: '',
        error: false,
        pass: true
    };
    try {
        const result = vm.run(`oracle(${person}, ${questionNumber});${code}`);
        if(typeof result !== 'boolean' || result !== correct) {
            ret.pass = false;
        }
    } catch {
        ret.message = 'Code threw error! Please resubmit!';
        ret.error = true;
        ret.pass = false;
    }
    return ret;
}

app.listen(80, function () {
    console.log('Autograder server listening on port 80!');
});