favorites.cats.forEach((cat) => {
    let img = document.createElement('img');
    img.src = cat;
    img.className = 'catimg';
    catholder.appendChild(img);
});


deletebtn.onclick = async () => {
    await fetch('/favorites.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        credentials: 'include',
        body: 'delete=true'
    })
    window.location.reload()
}