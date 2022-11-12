let token;

function sendUpdateScore(score) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "http://" + window.location.host + "/update-score");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({
        token: token,
        score: score
    }));
    xhr.onload = function() {
        res = JSON.parse(xhr.response);

        if (!res.ok) {
            window.location.href = "/error.html?error=" + res.error;
            return;
        } else if (res.flag) {
            window.location.href = "/flag.html?flag=" + res.flag;
            return
        }
    };
}

function updateScore(score) {
    if (!token) {
        let xhr = new XMLHttpRequest();
        xhr.open("GET", "http://" + window.location.host + "/get-token");
        xhr.send();
        xhr.onload = function() {
            let res = JSON.parse(xhr.response);
    
            if (!res.ok) {
                window.location.href = "/error.html?error=" + res.error;
                return;
            }
            token = res.token;
            sendUpdateScore(score);
        };
    } else {
        sendUpdateScore(score);
    }
}
