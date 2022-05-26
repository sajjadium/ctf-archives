const form = document.querySelector('#search-form');
const message = document.querySelector('#msg');
const table = document.querySelector('#results > tbody');

const byte2hex = [];
for (let i = 0; i < 256; i++) {
  byte2hex.push('%' + i.toString(16).toUpperCase().padStart(2, '0'));
}

const encode = (s) => {
  const gb = iconv.encode(s, 'GB18030');
  const octets = [];
  for (let i = 0; i < gb.length; i++) {
    octets.push(byte2hex[gb[i]]);
  }
  return octets.join('');
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const { query, submit } = e.target.elements;
  query.disabled = true;
  submit.disabled = true;
  message.innerText = 'Loading...';
  table.innerHTML = '';

  try {
    const res = await fetch(`/search.php?q=${encode(query.value)}`);
    if (res.status !== 200) throw ':(';

    const results = await res.json();
    if (results.length > 0) {
      for (const result of results) {
        const { book, chapter, number, chinese, english } = result;
        const info = [ book, chapter, number, chinese, english ];
        const row = table.insertRow();
        info.forEach(v => {
          const cell = row.insertCell();
          cell.innerText = v;
        });
      }
      message.innerText = `${results.length} result(s)`;
    } else {
      message.innerText = 'No results';
    }
  } catch (e) {
    message.innerText = 'Something went wrong!';
  }

  query.value = '';
  query.disabled = false;
  submit.disabled = false;
});
