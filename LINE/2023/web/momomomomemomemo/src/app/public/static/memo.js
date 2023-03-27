import GraphQL from './api.js'
const purl = window.purl

const memoId = purl().param('id')

const gql = new GraphQL(location.origin)

document.getElementById('memoBody').onload = function () {
    if (memoId) {
        gql.memo(memoId).then(res => {return res.json()}).then(data => {
            if (data.errors) {
                if (data.errors[0].extensions.code === 'UNAUTHORIZED') {
                    location.href = '/login'
                }
            } else {
                if (data.data.memo) {
                    document.getElementById('memo').innerText = data.data.memo.content
                } else {
                    location.href = '/'
                }
            }
        })
    } else {
        location.href = '/'
    }
}