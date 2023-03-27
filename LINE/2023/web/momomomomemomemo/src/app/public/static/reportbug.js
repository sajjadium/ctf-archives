import GraphQL from './api.js'

const bugReportErr = document.getElementById('bugReportErr')
const bugReportMsg = document.getElementById('bugReportMsg')
const captchaImg = document.getElementById('captchaImg')

const gql = new GraphQL(location.origin, {})


const updateCaptcha = () => {
    gql.getCaptchaImage().then(res => {return res.json()}).then(data => {
        if (data.errors) {
            if (data.errors[0].extensions.code === 'UNAUTHORIZED') {
                location.href = '/login'
            } else {
                bugReportErr.innerText = data.errors[0].message
            }
        } else {
            bugReportErr.innerText = ''
            captchaImg.setAttribute('src', data.data.getCaptchaImage)
        }
    })
}

document.getElementById('reportbugBody').onload = updateCaptcha

document.getElementById('reportButton').onclick = function () {
    const url = document.getElementById('url').value
    const captchaCode = document.getElementById('captchaCode').value
    
    if (url && captchaCode) {
        gql.reportBug(url, captchaCode).then(res => {return res.json()}).then(data => {
            if (data.errors) {
                bugReportErr.innerText = data.errors[0].message
                bugReportMsg.innerText = ''
            } else {
                bugReportErr.innerText = ''
                document.getElementById('captchaCode').value = ''
                bugReportMsg.innerText = 'Thank you for reporting!'
                updateCaptcha()
            }
        })
    }
}