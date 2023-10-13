
const resolveCallback = (credential) => {
    console.log(credential)


    fetch('https://tinder4cats.club/redeem.php', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `token=${credential.token}`
    })
    .then(response => response.text())
    .then(console.log)
    .catch(console.log)

    location.reload()
}

const rejectCallback = (error) => {
    console.log(error)
}

const fedcmlogin = () => {
    if (!'IdentityCredential' in window) {
        console.log('FedCM not supported!')
        return
    }
    navigator.credentials.get(
        {
            identity: {
                providers: [{
                    configURL: 'https://idp.agency/fedcm/config.php',
                    clientId: 'tinder4cats.club',
                    nonce: Math.floor(Math.random()*10**16)
                }],
                context: 'signin'
            },
            mediation: 'required'
        }
    )
    .then(resolveCallback)
    .catch(rejectCallback)
}



fedcmbtn.onclick = fedcmlogin
