const generate = (length) => {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

const queryString = window.location.search;
const parameters = new URLSearchParams(queryString);
const usernameLength = parameters.get('length');

// Generate a random username and display it
if (usernameLength === null) {
    var name = "loading...";
    window.location.href = "/?length=10";
}
else if (usernameLength.length > 0) {
    var name = generate(+usernameLength);
}
document.getElementById('generatedUsername').innerHTML = `Your generated username is: ${name}`;