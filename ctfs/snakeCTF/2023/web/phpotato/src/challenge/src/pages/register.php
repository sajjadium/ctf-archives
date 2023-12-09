<?php
// Page init hooks
register_init_hook($check_not_auth, [$_SESSION]);
execute_init_hooks();

// Logic handling
// Internal routing
// Render function
$render = fn() => print("
<html>
    <head>
        <title>Register</title>
        <link rel='stylesheet' href='assets/main.css'></style>
    </head>
    <body>
        <div class='navbar-wrapper'>
            <ul class='navbar'>
                <li class='navbar-item'><a href='login'>Login</a></li>
                <li class='navbar-item current'><a href='register'>Register</a></li>
            </ul>
        </div>
        <div class='main-form'>
        <p class='form-title'>Register</p>
            " . (isset($message) && $message != '' ?
    "<div class='message'>
                    <p>$message</p>
                </div>"
    : '')
    . "
            <form method='POST'>
                <input type='hidden' name='_METHOD' value='PUT'>
                <div class='form-entry'>
                    <label for='username'>Username</label>
                    <input type='text' name='username' class='box-input' />
                </div>
                <div class='form-entry'>
                    <label for='password'>Password</label>
                    <input type='password' name='password' class='box-input' />
                </div>
                <div class='form-entry'>
                    <input type='submit' name='register' class='submit box-input' value='Register'></input>
                </div>
            </form>
        </div>
    </body>
</html>
    ");
