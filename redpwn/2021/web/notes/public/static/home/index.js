(async () => {
  const load = new Promise((resolve) => {
    window.addEventListener('load', resolve);
  });

  let { login, username } = await (await fetch('/api/auth')).json();
  if (!login) window.location = '/';

  await load;

  const form = document.querySelector('form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = Object.fromEntries(new FormData(form));
    const response = await fetch('/api/notes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });
    const { error, message } = await response.json();
    if (error) alert(message);
    else alert('Note added.');
  });

  const anchor = document.querySelector('a');
  anchor.href = `/view/${username}`;
})();
