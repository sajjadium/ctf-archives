const { db, FIELDS } = require('./db_ops')
const { trivia } = require('./questions')
const { reportAnalytics } = require('./analytics')
const GOAL_POINTS = 1337;
const FLAG = process.env.FLAG || 'BSidesTLV2021{demo-flag-demo-flag-demo-flag}'

// utils

async function sanitizeInput(inputObj) {
    return {
        current_question: parseInt(inputObj.current_question) || 1,
        answer: parseInt(inputObj.answer) || 1,
        analytics: inputObj.analytics || []
    };
}

async function getState(gameId) {
    const question_id = await db.get_field(gameId, db.FIELDS.LEVEL);
    const score       = await db.get_field(gameId, db.FIELDS.SCORE);
    const triviaObj   = trivia[question_id] || false;
    return {
        question_id, 
        score, 
        triviaObj 
    }
}



// controllers / middlewares

async function get_questions(req, res, next) {
    const { gameId }  = req.user;
    const { score, question_id } = await getState(gameId);
    const respData = {
        question_id,
        score,
        GOAL_POINTS,
        trivia
    }

    return res.json(respData)
}

async function answer_question(req, res, next) {
    const { gameId }  = req.user;
    const { current_question, answer, analytics } = await sanitizeInput(req.body);
    const { question_id, triviaObj } = await getState(gameId);

    if(!triviaObj) { // make sure there are questions left
        res.status(501);
        res.json({ error: 'no more questions for you!'} );
    }

    else if(question_id != current_question) { // no skipping allowed!
        res.status(403);
        return res.json({error: `invalid current_question ${current_question} (expected: ${question_id})`});
    } 

    else if(!triviaObj.possible_answers.includes(answer)) { // accept only valid answers!
        res.status(403); 
        return res.json({error: `Invalid answer ${answer} (not one of possible_answers)`, possible_answers: triviaObj.possible_answers } );
    }

    else if(answer === triviaObj.correct_answer) {                              // if answer is correct
        await db.incr_field(gameId, db.FIELDS.SCORE, triviaObj.points);         // increase score
        await reportAnalytics(analytics);                                       // report analytics
        await db.incr_field(gameId, db.FIELDS.LEVEL, 1);                        // increase level
        return res.json({message: 'LEVEL-UP', points_added: triviaObj.points}); // return response
    } 

    else {
        res.status(403);
        return res.json({ error: 'Wrong answer' });
    }
}

async function get_flag(req, res, next) {
    const { gameId } = req.user;
    const   score    = await db.get_field(gameId, db.FIELDS.SCORE);

    if(parseInt(score) >= GOAL_POINTS) {
        return res.json({flag: FLAG});
    } else {
        return res.json({flag: 'ah, not yet (your points < 1337)'}); // no flag for you!
    }
}


// exporting relevant middlewares for server.js

const gameControls = {
    get_questions,
    answer_question,
    get_flag
}
module.exports = { gameControls }