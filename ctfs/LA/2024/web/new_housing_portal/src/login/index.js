const params = new URLSearchParams(location.search);

const err = params.get('err');
if (err) {
  const el = document.querySelector('.err');
  el.textContent = err;
  el.classList.remove('hidden');
}
