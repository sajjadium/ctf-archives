import GraphQL from './api.js'

const homeErr = document.getElementById('homeError')
const memoLi = document.getElementById('memoLi')
const memoArea = document.getElementById('memoArea')

const gql = new GraphQL(location.origin, {})

const syncMemos = () => {
    gql.memos().then(res => {return res.json()}).then(data => {
        if (data.errors) {
                if (data.errors[0].extensions.code === 'UNAUTHORIZED') {
                    location.href = '/login'
                } else {
                    homeErr.innerText = data.errors[0].message
                }
        } else {
            memoLi.innerHTML = ''
            data.data.memos.forEach(element => {
                let li = document.createElement('li')
                li.setAttribute('class', 'memo')
                li.innerText = element.content
                li.onclick = () => {
                    location.href = '/memo/?id=' + element.id
                }
                memoLi.appendChild(li)
            });
        }
    })
}

document.getElementById('homeBody').onload = syncMemos

document.getElementById('addMemoButton').onclick = () => {
    const content = memoArea.value

    if (content) {
        gql.addMemo(content).then(res => {return res.json()}).then(data => {
            if (data.errors) {
                homeErr.innerText = data.errors[0].message
            } else {
                memoArea.value = ''
                syncMemos()
            }
        })
    }
}
