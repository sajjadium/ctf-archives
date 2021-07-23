async function hide(ids) {
    await ids.forEach( async i => {
        document.getElementById(i).style.display = 'none';
    });
}

async function show(ids) {
    await ids.forEach( async i => {
        document.getElementById(i).style.display = 'block';
        document.getElementById(i).className = 'form'
    });
}

async function start_timer() {
    let seconds_left = 60;
    let interval = setInterval(function() {
    document.getElementById('timer').innerHTML = `<b style='color: red'>Time left</b>: ${seconds_left}s`;
    seconds_left--;
    if (seconds_left < 0) {
        clearInterval(interval);
        alert('Game Over! Re-directing back to main screen');
        document.location = '/';
    }
    }, 1000);
}


async function start_game() {
    return await new Promise((resolve, reject) => {
        fetch('/api/v1/start_game', {
            method: 'POST',
            body: JSON.stringify({})
        }).then(async res => {
            resolve(res.json());
        });
    });
}

async function update_stats() {
    document.getElementById('stats').innerHTML = `<b>Goal</b>: ${gameData.GOAL_POINTS} <br/><b>Your Score</b>: ${gameData.score}`;
    if(gameData.question_id > Object.keys(gameData.trivia).length) {
        await show(['get_flag', 'try_again']) 
        await hide(['start_game', 'game_desc', 'answer_val', 'send_answer', 'question']);
        alert('No more questions for you!')
        return ;
    }
    
    for(i in gameData.trivia) {
        if(i == gameData.question_id) { // rendering only what's necessary
            document.getElementById('question').innerHTML = gameData.trivia[i].content;
            document.getElementById('stats').innerHTML += `<br />Points for current question: ${gameData.trivia[i].points}`;
            let dropdown_opts = document.getElementById('answer_val');
            document.getElementById('send_answer').style.display = 'block'; 
            dropdown_opts.style.display = 'block';   

            for(j = 0; j < dropdown_opts.length; j++) {
                dropdown_opts.options[j].value = gameData.trivia[i].possible_answers[j]
                dropdown_opts.options[j].innerText = gameData.trivia[i].possible_answers[j]
            }
        }
    }
}

async function start_session() {
    await start_game().then(async res => {
        sessionStorage.setItem('accessToken', res.accessToken)
        window.gameData = await get_questions();
        await hide(['game_desc', 'start_game']);
        await update_stats()
        await start_timer();
    })
}

async function get_questions() {
    return await new Promise((resolve, reject) => {
        fetch('/api/v1/questions', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + sessionStorage.accessToken
            }
        }).then(async res => {
            resolve(res.json());
        });
    });
}


async function send_answer(answer) {
    return await new Promise((resolve, reject) => {
        fetch('/api/v1/answer', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + sessionStorage.accessToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                current_question: gameData.question_id,
                answer: parseInt(answer),
                // analytics: ['event_sending_answer', 'event_click']
            })
        }).then(async res => {
            resolve(res.json());
        });
    });
}

async function perform_send() {
    const dropdown      = await document.getElementById('answer_val');
    const users_answer  = dropdown.options[dropdown.options.selectedIndex].value;
    console.log(`SENDING :: ` , users_answer)
    let resp_data = await send_answer(users_answer);
    console.log(`resp data :: `, resp_data)
    if(resp_data.points_added) {
        window.gameData = await get_questions();
        await update_stats()
    } else if (resp_data.error) {
        alert(resp_data.error);
    } else {
        alert(JSON.stringify(resp_data))
    }
}

async function get_flag() {
    const fetch_flag = await new Promise((resolve, reject) => {
        fetch('/api/v1/flag', {
            headers: {
                'Authorization': 'Bearer ' + sessionStorage.accessToken
            } 
        }).then(async res => {
            resolve(res.json());
        });
    });
    alert(JSON.stringify(fetch_flag));
}


document.getElementById('start_game').addEventListener('click', start_session);
document.getElementById('send_answer').addEventListener('click', perform_send);
document.getElementById('get_flag').addEventListener('click', get_flag);

