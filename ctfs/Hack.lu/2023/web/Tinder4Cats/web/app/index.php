<?php 


include 'config.php';


if (!isset($_SESSION['user'])){
    header('Location: /login.php');
    die('Login first.');
}

?>
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Tinder4Cats</title>
    <link rel="stylesheet" href="/static/css/pico.min.css" />
    <link rel="stylesheet" href="/static/css/custom.css" />
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%2210 0 100 100%22><text y=%22.90em%22 font-size=%2290%22>🐈</text></svg>">
</head>
<body>
    <nav class="container-fluid">
        <ul>
            <li><a href="/" class="contrast">Home</a></li>
            <li><a href="/favorites.php">Favorites</a></li>
            <li><a href="/logout.php">Logout</a></li>
        </ul>
    </nav>
    <main class="container">
        <article>
            <header>
                <h1 class="welcome">Hi <?php echo $_SESSION['user']['username']; ?></h1> 
                <small><?php echo $_SESSION['user']['welcomemsg']; ?></small>
            </header>


            <div class="grid catholder">
                <img id="catimg" class="catimg"/>
            </div>
            <footer class="grid">
                <button id="likebtn" class="btn btn-primary">Like</button>
                <button id="nextbtn" class="btn btn-primary">Next</button>
            </footer>
        </article>
    </main>
    <script src="/static/js/main.js"></script>
</body>
</html>