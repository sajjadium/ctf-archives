if (!("initialised" in localStorage)) {
    Object.assign(localStorage, {
        blockHistory: "{}",
        initialised: true
    });
}
window.blockHistory = JSON.parse(localStorage.getItem("blockHistory"));

// stolen from https://stackoverflow.com/a/31102605
function sort(history) {
    return Object.keys(history).sort((a, b) => a-b).reduce((obj, key) => {
        obj[key] = history[key]; 
        return obj;
    }, {});
}

// patented 🅱️ad🅱️locker™ algorithm to add one history to another
function combineHistories(history, addedHistory) {
    for (const [date, record] of Object.entries(addedHistory)) {

        if (!(date in history)) history[date] = {};

        for (const [k, v] of Object.entries(record)) {
            history[date][k] = v; // 🅱️
        }
    }

    return history;
}

function showHistory(history, preview) {
    let historyHTML = "";

    // sort the history by date
    history = sort(history);

    if (preview) {
        // only show URLs and dates
        for (const [date, { url }] of Object.entries(history).reverse()) {
            historyHTML += `<p>${new Date(+date).toDateString()} - <code>${encodeURI(url)}</code></p>`;
        }
    }

    else {
        // show everything
        for (const [date, { url, numBlocked }] of Object.entries(history).reverse()) {
            historyHTML += `<p>${new Date(+date).toDateString()} - <code>${encodeURI(url)}</code><br>
                <b>${numBlocked} ads blocked</b></p>`;
        }
    }

    if (Object.keys(history).length === 0) {
        historyHTML = `<p>You have no history :(</p><var style="white-space: pre;">
            ⠀⣠⡶⠟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠻⢶⣄⠀
            ⣼⣿⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣿⣇
            ⣿⣿⣿⣿⣿⣿⠋⠉⠉⠉⠉⠛⠻⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⠀⠀⣶⣶⣶⡄⠀⢸⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⠀⠀⠛⠛⠛⠁⢠⣾⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⠀⠀⣶⣶⣶⣦⠀⠈⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⠀⠀⠻⠿⠟⠋⠀⢀⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⣦⣤⣤⣤⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿
            ⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟
            ⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀
        </var>`.replaceAll("    ", "");
    }

    // not a form but it looks nice :D
    document.body.innerHTML += `
        <fieldset id="historyContainer">
            <legend>History${preview ? " Preview" : ""}</legend>
            <div>${historyHTML}</div>
        </fieldset>
    `;
}
