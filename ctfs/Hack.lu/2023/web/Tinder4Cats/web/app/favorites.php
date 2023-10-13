<?php 


include 'config.php';


if (!isset($_SESSION['user'])){
    header('Location: /login.php');
    die('Login first.');
}

if (isset($_POST['like']) && is_string($_POST['like'])){
    // disable for admin and guest
    if ($_SESSION['user']['username'] === 'admin' || $_SESSION['user']['username'] === 'guest'){
        die();
    }
    db::add_favorites($_SESSION['user']['id'], $_POST['like']);
    die();
}

if (isset($_POST['delete'])){
    db::del_favorites($_SESSION['user']['id']);
    die();
}

?>
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Favorites</title>
    <link rel="stylesheet" href="/static/css/pico.min.css" />
    <link rel="stylesheet" href="/static/css/custom.css" />
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%2210 0 100 100%22><text y=%22.90em%22 font-size=%2290%22>🐈</text></svg>">
</head>
<body>
    <nav class="container-fluid">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/favorites.php" class="contrast">Favorites</a></li>
            <li><a href="/logout.php">Logout</a></li>
        </ul>
    </nav>
    <main class="container">
        <article>
            <header>
                <h1 class="welcome">Liked Cats</h1>
            </header>
            <div id="catholder"></div>
            <footer>
                <a id="deletebtn">Delete Favorites</a>
            </footer>
        </article>
    </main>
    <script src="/api.php?limit=10&offset=0"></script>
    <script src="/static/js/favorites.js"></script>
</body>
</html>