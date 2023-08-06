async function register(username, password) {
    const resp= await fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },

        credentials: "include",
        body: JSON.stringify({
            username,
            password
        }),
    })
    return await resp.json();
}

async function login(username, password) {
    const resp= await fetch('/login', {
        method: 'POST',

        credentials: "include",
headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username,
            password
        }),
    })

    const respJson=await resp.json()
    return respJson;
}

async function createProfile(first_name, last_name, profile_picture_link) {

        const resp= await fetch('/create-profile', {
            method: 'POST',
            credentials:"include",
headers: {
            'Content-Type': 'application/json'
        },
            body: JSON.stringify({
                first_name,
                last_name,
                profile_picture_link
            }),
        })

        return await resp.json()
}

async function report(url) {
    const resp = await fetch('/report', {
            method: 'POST',
            credentials:"include",
        headers: {
            'Content-Type': 'application/json'
        },
            body: JSON.stringify({
                url
            }),
        })


        return await resp.json()



}

async function makePublic() {

    const resp = await fetch('/make-public', {
        method: 'PATCH',
            credentials:"include",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            is_public: true
        })
        })
        return await resp.json()
}