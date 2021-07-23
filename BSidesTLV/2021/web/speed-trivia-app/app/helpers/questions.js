const trivia = {
   1: {
        content: 'How much is 1+1',
        possible_answers: [ 4, 2 ,1, 99 ],
        correct_answer: 2,
        points: 100
    }, 
    2: {
        content: 'How much is BSIDES + BSIDES',
        possible_answers: [ 11, 1337 , 99, 4 ],
        correct_answer: 1337,
        points: 200
    }, 
    3: {
        content: 'How much is SWAG * EXPLOIT',
        possible_answers: [ 11, 33 , 42, 7 ],
        correct_answer: 42,
        points: 1000
    },
    // Note: commented out the rest of the questions. 
    // Now they will never reach a score greater than GOAL_POINTS!
    /*
    4: {
        content: 'What year is it?',
        possible_answers: [ 1990, 2021 , 2099, 2012 ],
        correct_answer: 2021,
        points: 1000
    }
    
    */
};

module.exports = { trivia }