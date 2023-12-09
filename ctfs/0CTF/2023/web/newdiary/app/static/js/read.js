const param = new URLSearchParams(location.hash.slice(1));
const id = param.get('id');
if (id && /^[0-9a-f]+$/.test(id)) {
    fetch(`/read/${id}`).then(data => data.json()).then(data => {
        const title = document.createElement('p');
        title.innerText = data.title;
        document.getElementById("title").appendChild(title);

        const content = document.createElement('p');
        content.innerHTML = data.content;
        document.getElementById("content").appendChild(content);

    })
    document.getElementById("share").href = `/share_diary/${id}`;
}