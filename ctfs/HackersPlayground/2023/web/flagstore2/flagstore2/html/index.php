<?php
    include_once("config.php");
    include_once("auth_service.php");
    session_start();
?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Flag Store</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Color+Emoji&display=swap" rel="stylesheet">
    <script
      src="https://code.jquery.com/jquery-3.7.0.slim.min.js"
      integrity="sha256-tG5mcZUtJsZvyKAxYLVXrmjKBVLd6VpVccqz/r4ypFE="
      crossorigin="anonymous"></script>
    <link rel="stylesheet" href="/css/common.css">
    <style>

      .card-footer-item {
        font-family: 'Noto Color Emoji', sans-serif;
      }
    </style>
  </head>
  <body class="layout-documentation page-components">
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a class="navbar-item" href="/">
          FLAG STORE v2
        </a>

        <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" class="navbar-menu">
        <div class="navbar-start"></div>

        <div class="navbar-end">
          <?php if(!isset($_SESSION["username"])) { ?>
          <div id="navbar-nologin" class="navbar-item">
            <div class="buttons">
              <a class="button is-light" href="/login.php?auth_server=<?php echo $AUTH_SERVER; ?>">
                Log in
              </a>
            </div>
          </div>
            <?php } else {  ?>
          <div id="navbar-loggedin" class="navbar-item">
            <div class="buttons">
              <?php if($_SESSION["username"] == "admin") { ?>
              <a class="button is-warning" href="/admin/index.php">
                <span id="admin">Admin</span>
              </a>
              <?php } ?>
              <a class="button is-primary" href="/orders.php">
                🏳️ <span id="username">Cart</span>
              </a>
              <a class="button is-light" href="/logout.php">
                Log out
              </a>
            </div>
          </div>
            <?php } ?>
        </div>
      </div>
    </nav>

    <div class="content">
      <section class="hero is-dark">
        <div class="hero-body">
          <p class="title">
            FLAG STORE v2<span style="font-size: 4rem;">🏴‍☠️</span>
          </p>
        </div>
      </section>
      
      <section id="flags" class="section">
        <h1>🚧Sorry, our website is being redesigned.🚧</h1>
        <div id="flag-items" class="columns is-multiline"></div>

        <template id="flag-item-template">
          <div class="column is-2">
            <div class="card">
              <div class="flag-figure card-image">
                🇦🇫
              </div>
              <header class="card-header">
                <div class="card-header-title">
                  <div class="flag-title"></div>
                </div>
              </header>
              <div class="card-content">
                <div class="content">
                  <div class="flag-price title is-5 has-text-centered"></div>
                </div>
              </div>
              <div class="card-footer">
                <a class="card-footer-item button buy-button">Add 🛒</a>
              </div>
            </div>
          </div>
        </template>
      </section>

    </div>

    <script>
      function addCard(idx) {
        var form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "/orders.php");

        var idxField = document.createElement("input");
        idxField.setAttribute("type", "hidden");
        idxField.setAttribute("name", "idx");
        idxField.setAttribute("value", idx);

        var nameField = document.createElement("input");
        nameField.setAttribute("type", "hidden");
        nameField.setAttribute("name", "name");
        nameField.setAttribute("value", flags[idx].name);

        var flagField = document.createElement("input");
        flagField.setAttribute("type", "hidden");
        flagField.setAttribute("name", "price");
        flagField.setAttribute("value", flags[idx].price);

        form.appendChild(idxField);
        form.appendChild(nameField);
        form.appendChild(flagField);

        document.body.appendChild(form);
        form.submit();
      }
      
      function renderFlags(idx, flag){
          const t = document.getElementById('flag-item-template')
          const clone = document.importNode(t.content, true);
          clone.querySelector('.flag-figure').textContent = flag.flag
          clone.querySelector('.flag-title').textContent = flag.name
          clone.querySelector('.buy-button').href = `javascript:addCard(${idx})`
          clone.querySelector('.flag-price').textContent = flag.price
          return clone
       }
      const flags = [
        {"flag":"🏳️", "name":"White Flag", "price":"$1"},
        {"flag":"🏴", "name":"Black Flag", "price":"$4"},
        {"flag":"🏁", "name":"Chequered Flag", "price":"$200"},
      ];
      $(document).ready(() => {
        flags.forEach((flag, i) => {
            $('#flag-items').append(renderFlags(i, flag));
        });
      })

    </script>
  </body>
</html>
