const express          = require('express')
const jwt              = require('jsonwebtoken')
const { authControls } = require('./helpers/auth')
const { gameControls } = require('./helpers/game_controllers') 


const app = express();
app.use(express.json());
app.use(express.static('./public'))
app.use('/', function (req, res, next) {
        console.log('Request URL:', req.originalUrl)
        next();
});


app.post('/api/v1/start_game', authControls.start_session);


app.get('/api/v1/questions', 
        authControls.validate_jwt, 
        gameControls.get_questions);


app.post('/api/v1/answer', 
        authControls.validate_jwt, 
        gameControls.answer_question);


app.get('/api/v1/flag', 
        authControls.validate_jwt, 
        gameControls.get_flag);

app.listen(3000)