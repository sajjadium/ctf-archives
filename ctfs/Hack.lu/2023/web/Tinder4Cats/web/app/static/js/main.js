

API_URL = 'https://cataas.com/cat/cute?json=true'

const get_cat = async () => {
    likebtn.innerText = 'Like'
    let r = await fetch(API_URL)
    cat = await r.json()
    catimg.src = 'https://cataas.com' + cat.url
}


const fav_cat = async () => {
    let form = new FormData()
    await fetch('/favorites.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        credentials: 'include',
        body: 'like=https://cataas.com' + cat.url
    })
    likebtn.innerText = 'Liked!'
}


window.onload = nextbtn.onclick = get_cat
likebtn.onclick = fav_cat
