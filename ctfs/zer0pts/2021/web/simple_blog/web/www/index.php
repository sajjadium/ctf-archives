<?php
$nonce = base64_encode(random_bytes(20));
$theme = $_GET['theme'] ?? 'dark';
?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Simple Blog</title>
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; object-src 'none'; base-uri 'none'; script-src 'nonce-<?= $nonce ?>' 'strict-dynamic'; require-trusted-types-for 'script'; trusted-types default">
    <link rel="stylesheet" href="/css/bootstrap-<?= $theme ?>.min.css">
    <link rel="stylesheet" href="/css/style.css">
  </head>
  <body>
    <div class="container">
      <nav class="navbar navbar-expand-lg navbar-<?= $theme ?> bg-<?= $theme ?>">
        <a class="navbar-brand" href="/">Simple Blog</a>
        <ul class="navbar-nav mr-auto">
          <li class="nav-item"><a class="nav-link" href="/report.php">Report Vulnerability</a></li>
        </ul>
        <ul class="navbar-nav">
          <li class="nav-item"><a class="nav-link" href="/?theme=<?= $theme === 'dark' ? 'light' : 'dark' ?>">Toggle theme</a></li>
        </ul>
      </nav>
    </div>
    <main class="container" id="main">
      <div class="spinner-border" id="loading">
        <span class="sr-only">Loading...</span>
      </div>
    </main>
    <script src="/js/trustedtypes.build.js" nonce="<?= $nonce ?>" data-csp="require-trusted-types-for 'script'; trusted-types default"></script>
    <script nonce="<?= $nonce ?>">
    // JSONP
    const jsonp = (url, callback) => {
      const s = document.createElement('script');

      if (callback) {
        s.src = `${url}?callback=${callback}`;
      } else {
        s.src = url;
      }

      document.body.appendChild(s);
    };

    // render articles
    const render = articles => {
      const main = document.getElementById('main');
      const loading = document.getElementById('loading');

      articles.sort((a, b) => a.id - b.id);
      for (const article of articles) {
        const elm = document.createElement('article');
        elm.classList.add('blog-post');

        const title = document.createElement('h2');
        title.innerHTML = article.title;
        elm.appendChild(title);

        const content = document.createElement('p');
        content.innerHTML = article.content;
        elm.appendChild(content);

        main.appendChild(elm);
      }

      loading.remove();
    };

    // initialize blog
    const init = () => {
      // try to register trusted types
      try {
        trustedTypes.createPolicy('default', {
          createHTML(url) {
            return url.replace(/[<>]/g, '');
          },
          createScriptURL(url) {
            if (url.includes('callback')) {
              throw new Error('custom callback is unimplemented');
            }

            return url;
          }
        });
      } catch {
        if (!trustedTypes.defaultPolicy) {
          throw new Error('failed to register default policy');
        }
      }

      // TODO: implement custom callback
      jsonp('/api.php', window.callback);
    };

    init();
    </script>
  </body>
</html>