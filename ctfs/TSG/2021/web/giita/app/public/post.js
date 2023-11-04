const body = document.getElementById('body');
body.innerHTML = DOMPurify.sanitize(body.textContent);

hljs.highlightAll();
