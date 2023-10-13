<?php

ini_set('session.cookie_httponly', 1);
session_start();

if (isset($_SESSION['identity'])){
    header('Location: /');
    die('Already logged in.');
}


$identity_domain = getenv('IDENTITY_DOMAIN');
$app_domain = getenv('APP_DOMAIN'); 


$admin_identity =  [
    "id" => "1",
    "name" => "Admin Adminson",
    "email" => "admin@{$identity_domain}",
    "given_name" => "admin",
    "picture" => "https://{$identity_domain}/static/img/admin.png",
    "approved_clients" => [$app_domain],
    "login_hints" => ["admin", "admin@{$identity_domain}"]
];

$guest_identity = [ 
    "id" => "2",
    "name" => "Guest Guestson",
    "email" => "guest@{$identity_domain}",
    "given_name" => "guest",
    "picture" => "https://{$identity_domain}/static/img/guest.png",
    "approved_clients" => [$app_domain],
    "login_hints" => ["guest", "guest@{$identity_domain}"]

];



if (isset($_POST['username']) && is_string($_POST['username']) && isset($_POST['password']) && is_string($_POST['password'])){
    if($_POST['username'] === 'guest' && $_POST['password'] === 'guest'){
            $_SESSION['identity'] = $guest_identity;
            header('Location: /');
            die('Logged in.');
    }
    else if($_POST['username'] === 'admin' && $_POST['password'] === getenv('ADMIN_PASSWORD')){
            $_SESSION['identity'] = $admin_identity;
            header('Location: /');
            die('Logged in.');
    }
    else{
        $msg = 'Invalid username or password.';
    }
}



?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Identity Provider</title>
    <link rel="stylesheet" href="/static/css/custom.css" />
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%2210 0 100 100%22><text y=%22.90em%22 font-size=%2290%22>🆔</text></svg>">
</head>
<body>
<div class="container">
    <div class="card">
        <div class="pic">
            <img src="/static/img/idp.png">
        </div>

        <form method="POST">
            <input type="text" id="username" name="username" placeholder="Username" required autocomplete="username"/>
            <input type="password" id="password" name="password" placeholder="Password" required autocomplete="current-password"/>
            <div class="buttons">
                <button type="submit" id="submit" class="login-button">Login</button>
            </div>
            <?php if (isset($msg)){?>
            <blockquote>
            <?php echo $msg ?>
            </blockquote>
            <?php } ?>
        </form>

    </div>
</div>
</body>
</html>
