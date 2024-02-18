const login = ({ username, age }) =>
  fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username, age
    })
  })
    .then(r => r.json());

// bootleg jquery pepega
const $ = q => document.querySelector(q);
$('button').addEventListener('click', async () => {
  const username = $('[name=username]').value;
  const age = +$('[name=age]').value;

  const { msg } = await login({ username, age });
  if (!msg.includes('succe')) {
    $('.display').classList.remove('hide');
    $('.display img').classList.add('hide');
    $('.display .msg').textContent = msg;
    return;
  }

  const [ status, resp ] = await fetch('/img')
    .then(r => [r.status_code, r.json()]);
  const r = await resp;

  if (status == 400) {
    $('.display .msg').textContent = r.err;
    $('.display img').classList.add('hide');
    $('.display').classList.remove('hide');
    return;
  }
  $('.display .msg').textContent = r.msg;
  $('.display img').src = r.img;
  $('.display img').classList.remove('hide');
  $('.display').classList.remove('hide');
});
