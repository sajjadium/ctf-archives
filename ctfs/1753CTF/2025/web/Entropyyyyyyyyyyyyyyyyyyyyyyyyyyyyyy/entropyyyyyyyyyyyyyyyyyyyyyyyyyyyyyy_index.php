<?php

error_reporting(0);
ini_set('display_errors', 0);

session_start();

$usernameAdmin = 'admin';
$passwordAdmin = getenv('ADMIN_PASSWORD');

$entropy = 'additional-entropy-for-super-secure-passwords-you-will-never-guess';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    
    $hash = password_hash($usernameAdmin . $entropy . $passwordAdmin, PASSWORD_BCRYPT);
    
    if ($usernameAdmin === $username && 
        password_verify($username . $entropy . $password, $hash)) {
        $_SESSION['logged_in'] = true;
    }
}

?>

<!DOCTYPE html>
    <html>
    <head>
        <style>
            .welcome {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 24px;
                text-align: center;
            }

            body::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: url("bg.png");
                background-position: center;
                background-size: contain;
                background-repeat: no-repeat;
                z-index: -1;
                animation: spinBackground 120s linear infinite;
            }

            @keyframes spinBackground {
                from {
                    transform: rotate(0deg);
                }
                to {
                    transform: rotate(360deg);
                }
            }

            body {
                width: 100vw;
                height: 100vh;
                margin: 0;
                padding: 0;
                background-color:#0F2537;
                color: #EAAF30;
            }   

            .login-form {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 20px;
            border: 1px solid #EAAF30;
            border-radius: 5px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: inline-block;
            width: 150px;
        }
        input[type="submit"] {
            margin-left: 155px;
            background-color: #EAAF30;
            border: 0px;
            cursor: pointer;
        }

        </style>
    </head>
    <body>


<?php
if (isset($_SESSION['logged_in'])) {
?>

    <div class="welcome">Hello, Admin, here's your secret message:<br />
    <?php echo strval(getenv('flag')); ?> <br/><br/>Don't share it with anyone!</div>
<?php
} else {
?>
        <form class="login-form" method="POST">
            <div class="form-group">
                <label>User Name</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Paaaaaaasword</label>
                <input type="password" name="password" required>
            </div>
        <input type="submit" value="Sign In">
</form>
<?php } ?>
    
</body>
</html>

    
    
