<?php
session_start();
$_SESSION = array();
define('ADMIN_PASSWORD', 'f365691b6e7d8bc4e043ff1b75dc660708c1040e');

/* Router login API */
$req = @json_decode(file_get_contents("php://input"));
if (isset($req->username) && isset($req->password)) {
    if ($req->username === 'godmode'
        && !in_array($_SERVER['REMOTE_ADDR'], ['127.0.0.1', '::1'])) {
        /* Debug mode is not allowed from outside the router */
        $req->username = 'nobody';
    }

    switch ($req->username) {
        case 'godmode':
            /* No password is required in god mode */
            $_SESSION['login'] = true;
            $_SESSION['admin'] = true;
            break;

        case 'admin':
            /* Secret password is required in admin mode */
            if (sha1($req->password) === ADMIN_PASSWORD) {
                $_SESSION['login'] = true;
                $_SESSION['admin'] = true;
            }
            break;

        case 'guest':
            /* Guest mode (low privilege) */
            if ($req->password === 'guest') {
                $_SESSION['login'] = true;
                $_SESSION['admin'] = false;
            }
            break;
    }

    /* Return response */
    if (isset($_SESSION['login']) && $_SESSION['login'] === true) {
        echo json_encode(array('status'=>'success'));
        exit;
    } else {
        echo json_encode(array('status'=>'error'));
        exit;
    }
}
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>login - CAKEGEAR</title>
        <style>input { margin: 0.5em; }</style>
    </head>
    <body style="text-align: center;">
        <h1>CakeWiFi Login</h1>
        <div>
            <label>Username</label>
            <input type="text" id="username" required>
            <br>
            <label>Password</label>
            <input type="text" id="password" required>
            <br>
            <button onclick="login()">Login</button>
            <p style="color: red;" id="error-msg"></p>
        </div>
        <script>
         function login() {
             let error = document.getElementById('error-msg');
             let username = document.getElementById('username').value;
             let password = document.getElementById('password').value;
             let xhr = new XMLHttpRequest();
             xhr.addEventListener('load', function() {
                 let res = JSON.parse(this.response);
                 if (res.status === 'success') {
                     window.location.href = "/admin.php";
                 } else {
                     error.innerHTML = "Invalid credential";
                 }
             }, false);
             xhr.withCredentials = true;
             xhr.open('post', '/');
             xhr.send(JSON.stringify({ username, password }));
         }
        </script>
    </body>
</html>
