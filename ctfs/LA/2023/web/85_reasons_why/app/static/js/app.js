/* Add your Application JavaScript */

function show_error(message) {
    document.getElementById('status-text').innerHTML = message;
    document.getElementById('status-text').style = 'display: block;';
}

function redirect(endpoint) {
    window.location.replace(endpoint);
}
