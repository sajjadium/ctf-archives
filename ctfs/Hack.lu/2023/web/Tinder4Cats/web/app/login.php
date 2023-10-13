<?php


include 'config.php';

if (isset($_SESSION['user'])){
    header('Location: /');
    die('Already logged in.');
}

if (isset($_POST['username']) && is_string($_POST['username']) && isset($_POST['password']) && is_string($_POST['password'])){
    $user = db::login_user($_POST['username'], $_POST['password']);
    if ($user){
        $_SESSION['user'] = $user;
        header('Location: /');
        die();
    }
    else{
        $msg = 'Invalid username or password.';
    }
}


?>
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Login</title>
    <link rel="stylesheet" href="/static/css/pico.min.css" />
    <link rel="stylesheet" href="/static/css/custom.css" />
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%2210 0 100 100%22><text y=%22.90em%22 font-size=%2290%22>🐈</text></svg>">
</head>
<body>
    <nav class="container-fluid">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/login.php" class="contrast">Login</a></li>
            <li><a href="/register.php">Register</a></li>
            <li><a href="/logout.php">Logout</a></li>
        </ul>
    </nav>
    <main class="container">
        <article class="grid">
            <div>
                <hgroup>
                    <h1>Sign in</h1>
                    <h2>Do i know you?</h2>
                </hgroup>
                <form method="POST">
                    <input type="text" name="username" placeholder="Username" required autocomplete="username"/>
                    <input type="password" name="password" placeholder="Password" required autocomplete="current-password"/>
                    <button type="submit" class="contrast">Login</button>
                    <?php if (isset($msg)): ?>
                    <blockquote>
                    <?php echo $msg ?>
                    </blockquote>
                    <?php endif; ?>
                </form>
                <p>or</p>
                <button id="fedcmbtn">Login with <?php echo getenv('IDENTITY_DOMAIN');?></a>
            </div>
            <div>
                <img src="/static/img/hi.webp">
            </div>
        </article>
    </main>
</body>
<script src="/static/js/fedcm.js"></script>
</html>