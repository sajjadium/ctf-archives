function isInWindowContext() {
  const tmp = self;
  self = 1; // magic
  const res = (this !== self);
  self = tmp;
  return res;
}

// Ensure it is in window context with correct domain only :)
// Setting up variables and UI
if (isInWindowContext() && document.domain === '<%= domain %>') {
  const urlParams = new URLSearchParams(location.search);
  try { document.getElementById('error').innerText = urlParams.get('error'); } catch (e) {}
  try { document.getElementById('message').innerText = urlParams.get('message'); } catch (e) {}
  try { document.getElementById('_csrf').value = '<%= csrf %>'; } catch (e) {}
}