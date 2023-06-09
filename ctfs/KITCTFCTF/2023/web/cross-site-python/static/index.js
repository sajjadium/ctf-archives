const execButton = document.getElementById("exec");
const saveButton = document.getElementById("save");
const editButton = document.getElementById("edit");
const newButton = document.getElementById("new");


if (execButton !== null) {
    execButton.addEventListener("click", (e) => {
        sourcecode = document.getElementById("text");
        if (sourcecode !== null) {
            let temp = window.location.href.split("/");
            temp[temp.length - 1] = "save";
            url = temp.join("/");
            fetch(url, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                method: "POST",
                body: JSON.stringify({"code": sourcecode.value}),
            }).then( () => {
                let temp = window.location.href.split("/");
                temp[temp.length - 1] = "exec";
                window.location.href = temp.join("/");
            });
        }
    });
}

if (saveButton !== null) {
    saveButton.addEventListener('click', (e) => {
        sourcecode = document.getElementById("text");
        if (sourcecode !== null) {
            let temp = window.location.href.split("/");
            temp[temp.length - 1] = "save";
            url = temp.join("/");
            fetch(url, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                method: "POST",
                body: JSON.stringify({"code": sourcecode.value}),
            });
        }
    });
}

if (editButton !== null) {
    editButton.addEventListener('click', (e) => {
        let temp = window.location.href.split("/");
        temp[temp.length - 1] = "edit"
        window.location.href = temp.join("/")
    });
}

if (newButton !== null) {
    newButton.addEventListener('click', (e) => {
        window.location.href = "/new"
    });
}

