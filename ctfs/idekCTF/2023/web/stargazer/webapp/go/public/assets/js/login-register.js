const toggleForm = () => {
    const container = document.querySelector(".container");
    container.classList.toggle("active");
};

onsubmit = () => {
    return false
}



let csrf = document.querySelector('meta[name=csrf-token]').content

const login = async () => {
    let res = await (await fetch('/login', {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf
        },
        body: JSON.stringify({
            "username": document.getElementById('username-login').value,
            "password": document.getElementById('password-login').value,
        })
    })).json()

    if(res.path){
        window.location.href = res.path
    }else{
        alert(res.message)
    }
}

const register = async () => {
    let res = await (await fetch('/register', {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': csrf
        },
        body: JSON.stringify({
            "username": document.getElementById('username-register').value,
            "password": document.getElementById('password-register').value
        })
    })).json()

    if(res.path){
        window.location.href = res.path
    }else{
        alert(res.message)
    }
}

document.querySelector('#register').onsubmit = (e) => {
    register()
}

document.querySelector('#login').onsubmit = (e) => {
    login()
}

document.querySelector('.toogle').onclick = (e) => {
    toggleForm()
}

document.querySelector('#toogle').onclick = (e) => {
    toggleForm()
}