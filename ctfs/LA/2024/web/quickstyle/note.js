const params = new URLSearchParams(location.search);
const url = params.get('page');

setTimeout(async () => {
  if (!url) return;
  const message = await fetch(url).then(r => r.text());
  if (message.length > 6000000) return;
  document.querySelectorAll('.message')[0].innerHTML = message;
  document.querySelectorAll('style').forEach(s => s.remove());
}, 10);
