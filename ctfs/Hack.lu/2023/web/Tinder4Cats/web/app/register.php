<?php


include 'config.php';

if (isset($_SESSION['user'])){
    header('Location: /');
    die('Already logged in.');
}

if (isset($_POST['username']) && is_string($_POST['username']) && isset($_POST['password']) && is_string($_POST['password'])){
    if(db::get_user($_POST['username'])){
        $msg = 'Username already exists.';
    }
    elseif (strlen($_POST['username']) < 6){
        $msg = 'Username is too short.';
    }
    elseif (strlen($_POST['password']) < 8){
        $msg = 'Password is too short.';
    }
    else{
        db::add_user($_POST['username'], $_POST['password'], 'Welcome to the site.');
        header('Location: /login.php');
        die('Succressfully registered.');
    }
}
?>

<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Register</title>
    <link rel="stylesheet" href="/static/css/pico.min.css" />
    <link rel="stylesheet" href="/static/css/custom.css" />
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%2210 0 100 100%22><text y=%22.90em%22 font-size=%2290%22>🐈</text></svg>">
</head>
<body>
    <nav class="container-fluid">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/login.php">Login</a></li>
            <li><a href="/register.php" class="contrast">Register</a></li>
            <li><a href="/logout.php">Logout</a></li>
        </ul>
    </nav>
    <main class="container">
        <article class="grid">
            <div>
                <hgroup>
                    <h1>Register</h1>
                    <h2>Welcome !?</h2>
                </hgroup>
                <form method="POST">
                    <input type="text" name="username" minlength="6" placeholder="Username" required autocomplete="username"/>
                    <input type="password" name="password" minlength="8" placeholder="Password" required autocomplete="new-password"/>
                    <input type="password" id="confirm" placeholder="Confirm Password" autocomplete="new-password" />
                    <button type="submit" class="contrast">Register</button>
                    <?php if (isset($msg)): ?>
                    <blockquote>
                    <?php echo $msg ?>
                    </blockquote>
                    <?php endif; ?>
                </form>
            </div>
            <div>
                <img src="/static/img/hi.webp">
            </div>
        </article>
    </main>
</body>

</html>