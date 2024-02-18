const $ = q => document.querySelector(q);

$('.search input[name=username]').addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    location.search = '?q=' + encodeURIComponent(e.target.value);
  }
});

const params = new URLSearchParams(location.search);
const query = params.get('q');
if (query) {
  (async () => {
    const user = await fetch('/user?q=' + encodeURIComponent(query))
      .then(r => r.json());
    if ('err' in user) {
      $('.err').innerHTML = user.err;
      $('.err').classList.remove('hidden');
      return;
    }
    $('.user input[name=username]').value = user.username;
    $('span.name').innerHTML = user.name;
    $('span.username').innerHTML = user.username;
    $('.user').classList.remove('hidden');
  })();
}
