/* ** Utils ** */
var noHTML = (s) => {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

var handleSuccess = (m) => {
    msg.innerHTML = `<div class="alert alert-success" role="alert">
        ${noHTML(m)}
    </div>`;
}

var handleError = (m) => {
    msg.innerHTML = `<div class="alert alert-danger" role="alert">
        ${noHTML(m)}
    </div>`;
}

var handleNotes = (user, notes) => {
    var parse = (note) => {
        return `<tr>
            <td>
            <p class="fw-normal mb-1">${noHTML(note[1])}</p>
            <p class="text-muted mb-0">${noHTML(user)}</p>
            </td>
            <td>
            <span class="badge badge-success rounded-pill d-inline">Active</span>
            </td>
            <td>${noHTML(note[2])}</td>
            <td>
            <a href="/note/${noHTML(note[0])}" class="btn btn-link btn-sm btn-rounded">
                Edit
            </a>
            </td>
        </tr>`
    }

    output.innerHTML = `${notes.map(note => parse(note)).join("")}`;
}

/* ** Routes ** */
var fetchAPI = async (path, method, data) => {
    var options = {};
    options.method = method;
    options.headers = {}
    options.headers["Content-Type"]  = "application/json";
    if (data)
        options.body = JSON.stringify(data);

    var bearer = localStorage.getItem("bearer");
    if (bearer)
        options.headers["Authorization"] = `Bearer ${bearer}`;

    return fetch(path, options).then(d => d.json()).then((d) => { return d });
}


var loginAPI = async (username, password) => {
    var res = await fetchAPI("/api/login", "POST", {
        "username": username,
        "password": password
    })

    if (res["error"])
        handleError(res["error"]);

    if (res["bearer"]) {
        localStorage.setItem("bearer", res["bearer"]);
        location.href = "/notes";
    }
}


var registerAPI = async (username, password) => {
    var res = await fetchAPI("/api/register", "POST", {
        "username": username,
        "password": password
    })

    if (res["error"])
        handleError(res["error"]);

    if (res["success"])
        handleSuccess(res["success"]);
}


var logoutAPI = () => {
    localStorage.clear();
    location.href = "/logout?r=/login";
}


var profileAPI = async (user) => {
    var res = await fetchAPI(`/api/user/${user}`, "GET")
    
    handleNotes(user, res["notes"]);

    return res["notes"]
}


var createNoteAPI = async (user, name) => {
    var res = await fetchAPI(`/api/user/${user}/create`, "POST", {
        "name": name
    })

    if (res["error"])
        handleError(res["error"]);

    if (res["success"])
        handleSuccess(res["success"]);
}


var loadNoteAPI = async (user, uuid) => {
    var res = await fetchAPI(`/api/user/${user}/${uuid}`, "GET")

    title_input.value = res["title"];
    content_input.innerText = res["content"];
}


var editNoteAPI = async(user, uuid, title, content) => {
    var res = await fetchAPI(`/api/user/${user}/${uuid}/edit`, "POST", {
        "title": title,
        "content": content
    })

    if (res["error"])
        handleError(res["error"]);

    if (res["success"])
        handleSuccess(res["success"]);
}
