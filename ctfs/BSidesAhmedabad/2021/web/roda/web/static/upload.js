window.addEventListener('load', () => {
  const drop = document.getElementById('drop');
  const message = document.getElementById('message');

  function showError(text) {
    message.textContent = text;
    message.classList.remove('hidden');
  }

  drop.addEventListener('drop', async (e) => {
    e.preventDefault();

    if (e.dataTransfer.items) {
      const item = e.dataTransfer.items[0];
      if (item.kind !== 'file') {
        showError('Please upload a file');
        return;
      }

      const file = item.getAsFile();
      const formData = new FormData();
      formData.append('file', file);

      const result = await (await fetch('/upload', {
        method: 'POST',
        body: formData
      })).json();

      if (result.status === 'success') {
        location.assign('/' + result.id);
      } else {
        showError(result.message);
      }
    }
  }, false);

  drop.addEventListener('dragover', (e) => {
    e.preventDefault();
  }, false);
}, false);

