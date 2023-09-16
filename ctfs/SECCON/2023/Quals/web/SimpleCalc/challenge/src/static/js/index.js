const params = new URLSearchParams(location.search);
const result = eval(params.get('expr'));
document.getElementById('result').innerText = result.toString();
