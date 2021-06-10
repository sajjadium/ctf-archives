(async () => {

  await new Promise((resolve) => {
    window.addEventListener('load', resolve);
  });

  document.getElementById('text-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = document.getElementById('text-input').value;
    const res = await (await fetch('/api/createPaste', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        data: text
      })
    })).json();

    if (res.error) {
      return;
    }

    document.getElementById('output').textContent =
      `${window.origin}/view/${res.data}`
  });

})();
