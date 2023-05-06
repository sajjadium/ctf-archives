async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        mode: 'no-cors',
        credentials: 'omit',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data) 
    })
    .then(response => {return true})
    .catch((error) => {
        return false
    });
    return response;
}

async function getData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'GET',
        mode: 'cors',
        credentials: 'omit',
        referrerPolicy: 'no-referrer'
    })
    .then(response => {return response.json()})
    .catch((error) => {
        return false
    });
    return response;
}

window.addEventListener("load", function(e){
    document.querySelector("#purge-cache-form").addEventListener("submit", function(e){
        e.preventDefault();
        postData('https://cloudflare-dns.com/api/v1/purge?type=A&domain='+domain.value, {})
        .then(data => {
          document.querySelector("#info-message").innerText = `This whole city (${domain.value}) has been purged!`;
        });
        return false;
    });
    document.querySelector("#lookup-name-form").addEventListener("submit", function(e){
        e.preventDefault();
        getData(location.pathname+'/api/lookup/'+domain.value, {})
        .then(data => {
          document.querySelector("#info-message").innerText = JSON.stringify(data, null, 2);
        });
        return false;
    });
});