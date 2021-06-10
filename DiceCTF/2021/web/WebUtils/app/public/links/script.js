(async () => {

  await new Promise((resolve) => {
    window.addEventListener('load', resolve);
  });

  document.getElementById('url-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = document.getElementById('url-input').value;
    const res = await (await fetch('/api/createLink', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        data: url
      })
    })).json();

    if (res.error) {
      return;
    }

    document.getElementById('output').textContent =
      `${window.origin}/view/${res.data}`
  });

})();
