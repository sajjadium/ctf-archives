import validator from 'validator'

export function validateEmail(email) {
    return validator.isEmail(email)
}

function validateUsername(username) {
    return validator.isAlphanumeric(username, 'en-US') && username.length > 3 && username.length < 30
}

function validatePassword(password) {
    return validator.isAlphanumeric(password, 'en-US') && password.length > 6 && password.length < 30
}

export function validateLogin(username, password) {
    return username && password && validateUsername(username) && validatePassword(password)
}