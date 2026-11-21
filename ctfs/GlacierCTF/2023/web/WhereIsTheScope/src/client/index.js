// ###########
// ## PLAYER
// ###########

function updateQuery(uri) {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set("source", "youtube");
    urlParams.set("uri", uri);
    window.location.search = urlParams;
}

function loadFromQuery() {
    const query = new URLSearchParams(window.location.search);
    const source = query.get("source") || "youtube";
    const uri = query.get("uri");
    document.getElementById("searchInput").value = uri || "https://www.youtube.com/embed/dQw4w9WgXcQ?&autoplay=1";
    if(!uri) return false;
    updateSource(uri, source);
    var ifconfig = {
        pathname: `<iframe frameborder="0" width=950 height=570 src="${parseURI(uri)}"></iframe>`
    }
    document.getElementById("viewer").srcdoc = ifconfig.pathname;
    return true;
}

function parseURI(uri) {
    const uriParts = new URL(uri);
    if(uriParts.origin === "https://www.youtube.com")
        return uri;
    // If user does not provide a youtube uri, we take the default one.
    return "https://www.youtube.com/embed/dQw4w9WgXcQ?&autoplay=1";
}

function updateSource(uri, source_provider) {
    const source = document.querySelector(".source-link");
    source.id = source_provider;
    source.href = uri;
}

function loadVideo(videoURI) {
    const ifconfig = {
        pathname: `<iframe frameborder="0" width=950 height=570 src="${parseURI(videoURI)}"></iframe>`
    };
    document.getElementById("viewer").srcdoc = ifconfig.pathname;
}

function onSearch() {
    const input = document.getElementById("searchInput").value;
    updateQuery(input);
    updateSource(input, "youtube");
    loadVideo(input);
}

function onReportClick() {
    document.getElementById("reportBtn").addEventListener("click", _ => {
        alert('Thank you for reporting this uri. A moderator will review it soon.')
        fetch("/report", {
            headers: {
                "Content-Type": "application/json"
            },
            method: "POST",
            body: JSON.stringify({
                path: window.location.search
            })
        });
    })
}

function __readyPlayer() {
    document.getElementById("searchInput").addEventListener("keyup", e => {
        if(e.key === "Enter")
            onSearch();
    })
    document.getElementById("search").addEventListener("click", _ => {
        onSearch();
    })
    if(!loadFromQuery())
        onSearch();
    onReportClick();
}

// ###########
// ## 2FA
// ###########

function __on_2fa_click() {
    document.getElementById("setup_2fa").addEventListener("click", _ => {
        fetch("/setup_2fa", {
            method: "POST"
        }).then(res => {
            if(res.status === 400) return alert("You already have requested an 2FA token!")
            return res.json();
        }).then(json => {
            if(!json) return;
            new QRCode(document.getElementById("qrcode_2fa"), json.totp)
            document.getElementById("fa_note").style.display = "block";
        })
    })
}

// ###########
// ## NOTES
// ###########

function saveNotes() {
    const notesContent = document.getElementById("notes_content");
    const message = notesContent.value;
    const payload = {message};
    fetch("/secret_note", {
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify(payload)
    }).then(res => {
        console.log(res);
        if(res.status === 204) {
            alert("Note saved.");
        } else {
            alert("Could not save note.")
        }
    })
}

function loadNotes() {
    // TODO: Implement load notes
    alert("This feature is currently under development and will be available soon.")
}

function __onLoadNotes() {
    const notesLoad = document.getElementById("notes_load");
    notesLoad.addEventListener("click", _ => {
        loadNotes();
    });    
}

function __onSaveNotes() {
    const notesSubmit = document.getElementById("notes_submit");
    notesSubmit.addEventListener("click", _ => {
        saveNotes();
    });
}

// ###########
// ## DOM Related Events
// ###########

window.addEventListener("load", _ => {
    __readyPlayer();
    __on_2fa_click();
    __onSaveNotes();
    __onLoadNotes();
});