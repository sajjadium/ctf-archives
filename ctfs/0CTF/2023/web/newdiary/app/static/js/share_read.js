load = () => {
    document.getElementById("title").innerHTML = ""
    document.getElementById("content").innerHTML = ""
    const param = new URLSearchParams(location.hash.slice(1));
    const id = param.get('id');
    let username = param.get('username');
    if (id && /^[0-9a-f]+$/.test(id)) {
        if (username === null) {
            fetch(`/share/read/${id}`).then(data => data.json()).then(data => {
                const title = document.createElement('p');
                title.innerText = data.title;
                document.getElementById("title").appendChild(title);
        
                const content = document.createElement('p');
                content.innerHTML = data.content;
                document.getElementById("content").appendChild(content);
            })
        } else {
            fetch(`/share/read/${id}?username=${username}`).then(data => data.json()).then(data => {
                const title = document.createElement('p');
                title.innerText = data.title;
                document.getElementById("title").appendChild(title);

                const content = document.createElement('p');
                content.innerHTML = data.content;
                document.getElementById("content").appendChild(content);
            })
        }
        document.getElementById("report").href = `/report?id=${id}&username=${username}`;
    }
    window.removeEventListener('hashchange', load);
}
load();
window.addEventListener('hashchange', load);