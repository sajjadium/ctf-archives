import GraphQL from './api.js'

const loginErr = document.getElementById('loginError')
const loginMsg = document.getElementById('loginMsg')

const gql = new GraphQL(location.origin, {})

document.getElementById('registerButton').onclick = function () {
    const username = document.getElementById('username').value
    const password = document.getElementById('password').value
    
    if (username && password) {
        gql.register(username, password).then(res => {return res.json()}).then(data => {
            if (data.errors) {
                loginErr.innerText = data.errors[0].message
                loginMsg.innerText = ''
            } else {
                loginErr.innerText = ''
                loginMsg.innerText = 'Registration succeed! Login!'
            }
        })
    }
}

document.getElementById('loginButton').onclick = function () {
    const username = document.getElementById('username').value
    const password = document.getElementById('password').value
    
    if (username && password) {
        gql.login(username, password).then(res => {return res.json()}).then(data => {
            if (data.errors) {
                loginErr.innerText = data.errors[0].message
                loginMsg.innerText = ''
            } else {
                gql.token = data.data.login
                location.href = '/'
            }
        })
    }
}