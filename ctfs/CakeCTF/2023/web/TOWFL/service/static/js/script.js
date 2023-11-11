let submission;

/* Set every radio button unchecked */
function resetRadioButtons() {
    for (let i = 0; i < 10; i++) {
        for (let j = 0; j < 4; j++) {
            document.getElementById(`exam-ans-${i+1}-${j+1}`).checked = false;
        }
    }
}

/* Save selections of the current question */
function saveStateLocal(n) {
    for (let i = 0; i < 10; i++) {
        for (let j = 0; j < 4; j++) {
            const l = document.getElementById(`exam-ans-${i+1}-${j+1}`);
            if (l.checked === true) {
                submission[n-1][i] = j;
                break;
            }
        }
    }
}

/* Submit answers and get the score */
async function submitAnswers() {
    // Submit answers
    let res = await fetch('/api/submit', {
        method: 'POST', credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(submission)
    });
    if (!res.ok) { alert("Server error"); return; }
    let json = await res.json();
    if (json.status !== 'ok') { alert(`Server error: ${json.reason}`); return; }

    // Get score
    res = await fetch('/api/score', {
        method: 'GET', credentials: 'include',
    });
    if (!res.ok) { alert("Server error"); return; }
    json = await res.json();
    if (json.status !== 'ok') { alert(`Server error: ${json.reason}`); return; }

    // Display score
    document.getElementById('exam').hidden = true;
    document.getElementById('score-value').innerText = `${json.data.score}`;
    document.getElementById('flag').innerText = json.data.flag;
    document.getElementById('score').hidden = false;
}

/* Load a set of questions */
async function loadNthQuestion(n) {
    // Get questions
    let res = await fetch(`/api/question/${n}`, { credentials: 'include' });
    if (!res.ok) { alert("Server error"); return; }
    let json = await res.json();
    if (json.status !== 'ok') { alert(`Server error: ${json.reason}`); return; }

    // Display questions
    document.getElementById('exam-passage').innerText = json.data.passage;
    for (let i = 0; i < 10; i++) {
        document.getElementById(`exam-question-${i+1}`)
            .innerText = json.data.questions[i].question;
        for (let j = 0; j < 4; j++) {
            document.getElementById(`exam-question-${i+1}-${j+1}`)
                .innerText = json.data.questions[i].options[j];
            document.getElementById(`exam-ans-${i+1}-${j+1}`)
                .checked = submission[n-1][i] === j;
        }
    }

    // Create "submit" or "go to next" button
    const submit = document.getElementById('submit');
    if (n == 10) {
        submit.innerText = "Submit";
        submit.onclick = () => {
            saveStateLocal(n);
            submitAnswers();
        }
    } else {
        submit.innerText = "Go To Next";
        submit.onclick = () => {
            saveStateLocal(n);
            document.getElementById(`q${n+1}`).click();
            window.scroll({top: 0, behavior: 'smooth'});
        }
    }

    // Show the current link in red
    for (let i = 1; i <= 10; i++) {
        if (i == n) {
            document.getElementById(`q${i}`).children[0].style.color = "red";
        } else {
            document.getElementById(`q${i}`).children[0].style.color = "blue";
        }
    }
}

/* Set onclick handlers */
for (let i = 1; i <= 10; i++) {
    document.getElementById(`q${i}`).onclick = async () => {
        resetRadioButtons();
        await loadNthQuestion(i);
    }
}
document.getElementById('btn-start').onclick = async () => {
    // Start the exam
    let res = await fetch('/api/start', {
        method: 'POST', credentials: 'include'
    });
    if (!res.ok) { alert("Server error"); return; }
    let json = await res.json();
    if (json.status !== 'ok') { alert(`Server error: ${json.reason}`); return; }
    document.getElementById('start').hidden = true;
    document.getElementById('exam').hidden = false;

    // Reset the state
    submission = [];
    for (let i = 0; i < 10; i++) {
        submission.push([]);
        for (let j = 0; j < 10; j++) {
            submission[i].push(null);
        }
    }

    // Display the first question
    resetRadioButtons();
    loadNthQuestion(1);
}
