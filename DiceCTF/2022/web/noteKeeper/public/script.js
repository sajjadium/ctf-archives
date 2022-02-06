let $ = document.querySelector.bind(document); // imagine using jQuery

const login = () => ($("#form").action = "/api/login") && $("#form").submit();
const register = () => ($("#form").action = "/api/register") && $("#form").submit();

const newNote = () => ($("#note-textarea").value = $("#note-div").innerText) && $("#note-form").submit();

const loadAudio = () => {
    let a = new Audio("/api/audio/file?" + (+Date.now())); // cache buster
    a.controls = true;
    a.onloadeddata = () => {
        $("#audio").classList.remove("d-none");
        $("#audio-zone").appendChild(a);
    };
};

window.onload = () => {
    $("#login") && ($("#login").onclick = login);
    $("#register") && ($("#register").onclick = register);

    $("#note-submit") && ($("#note-submit").onclick = newNote);
};

const load_alerts = (data) => {
    if(data) {
        let { msg, type = 'primary' } = data;
        $("#alert").innerText = msg;
        $("#alert").classList.toggle("alert-" + type);
        $("#alert").classList.toggle("d-none");
    }
};

const load_user = (user) => {
    // check for audio once only
    if(!$("#username").innerHTML) {
        $("#username").innerHTML = user;
        loadAudio();
    }
};

const load_notes = (notes) => {
    if(!notes) return;

    let ul = document.createElement("ul");
    notes.forEach((note, i) => {
        let li = document.createElement("li");

        let div = document.createElement("div");
        div.className = "note";

        let icon = document.createElement("i");
        icon.className = "note-trash fa fa-trash";
        icon.innerHTML = "&nbsp;";

        let span = document.createElement("span");
        span.innerText = note;

        div.onclick = async () => {
            await fetch("/api/notes/remove", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: "index=" + i
            });
            location.reload();
        };

        div.appendChild(icon);
        div.appendChild(span);

        li.appendChild(div);
        ul.appendChild(li);
    });
    $("#notes").appendChild(ul);
};
