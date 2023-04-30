var input = document.getElementById('command');
var output = document.getElementById("console-output");

document.getElementById("command").addEventListener('keydown', (e) => {
  if (e.keyCode === 13) {

    let host = input.value;

    try {
      new URL(host);
    } catch {
      return output.innerHTML = "Illegal Characters Detected";
    }

    output.innerHTML = '';

    fetch('/api/curl', {
      method: 'POST',
      body: `ip=${host}`,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    .then(resp => resp.json())
    .then(data => {
      output.innerHTML = data.message;
    });

    input.value = '';
  }
});
