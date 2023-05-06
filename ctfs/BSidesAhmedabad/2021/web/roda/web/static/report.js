async function onSubmit(token) {
  const button = document.getElementById('recaptcha');
  button.disabled = true;

  const result = await (await fetch(location.pathname + '/report?token=' + token, {
    method: 'POST'
  })).json();
  button.textContent = '\u{1f6a9}Thanks for the report! Queue length: ' + result.length;
  button.disabled = true;
}