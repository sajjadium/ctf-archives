function submitLink(e) {
    input_url_val = input_url.value;

    error_client.setAttribute('hidden', 'true')
    error_server.setAttribute('hidden', 'true')
    result.setAttribute('hidden', 'true')

    if (input_url_val === undefined) {
        error_client.hidden = false;
    }

    fetch("/upload?" + new URLSearchParams({ url: input_url_val }), {
        method: 'POST'
    }).then(res => {
        if (res.status >= 400 && res.status <= 499) {
            error_client.removeAttribute('hidden');
        } else if (res.status > 500) {
            error_server.removeAttribute('hidden');
        } else if (res.status == 200) {
            return res.json()
        }
    }).then(json => {
        if (json !== undefined) {
            result.innerHTML = `<p>Your extended url: <a href=${json.url}>${json.url}</a>.</p>`
            result.removeAttribute('hidden');
        }
    })
}