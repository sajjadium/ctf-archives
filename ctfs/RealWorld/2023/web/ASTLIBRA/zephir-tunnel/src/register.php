<?php
require_once('config.php');
if(isset($_POST['username']) && isset($_POST['password'])){
    $username = (string) $_POST['username'];
    $password = (string) $_POST['password'];
    if(strlen($username) < 5 || strlen($username) > 20){
        die('Username must be between 5 and 20 characters');
    }
    if (preg_match('/[^a-zA-Z0-9_]/', $username)) {
        die('Invalid characters in username');
    }
    // the first byte of the username must be a letter
    if (!preg_match('/[a-zA-Z]/', $username[0])) {
        die('Username must start with a letter');
    }
    if(strlen($password) < 5 || strlen($password) > 20){
        die('Password must be between 5 and 20 characters');
    }
    // check if username already exists
    $sql = "SELECT * FROM users WHERE username = ?";
    $stmt = $dbc->prepare($sql);
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();
    if($result->num_rows > 0){
        die('Username already exists');
    }
    // insert user into database
    $sql = "INSERT INTO users (username, password) VALUES (?, ?)";
    $stmt = $dbc->prepare($sql);
    $stmt->bind_param("ss", $username, $password);
    $stmt->execute();
    header('Location: login.php');
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="shortcut icon" href="assets/images/favicon.ico" type="image/x-icon">
    <title>Register</title>

    <!-- Vendor css -->
    <link rel="stylesheet" href="./src/vendors/@mdi/font/css/materialdesignicons.min.css">

    <!-- Base css with customised bootstrap included -->
    <link rel="stylesheet" href="./src/css/miri-ui-kit-free.css">

    <!-- Stylesheet for demo page specific css -->
    <link rel="stylesheet" href="./assets/css/demo.css">
</head>
<body class="login-page">

    <div class="card login-card">
        <div class="card-body">
            <h3 class="text-center text-white font-weight-light mb-4">Register</h3>
            <form action="register.php" method="POST">
                <div class="form-group">
                    <input type="text" name="username" placeholder="Username" class="form-control">
                </div>
                <div class="form-group">
                    <input type="text" name="password" placeholder="Password" class="form-control">
                </div>
                <input type="submit" value="Register" class="btn btn-danger btn-block mb-3">
            </form>
            <div class="d-flex justify-content-between mt-4">
                <a class="text-white text-center font-weight-light" href="login.php">Log in</a>
        
            </div>
        </div>
    </div>
    <footer>
        <div class="container">
            <nav class="navbar navbar-dark bg-transparent navbar-expand footer-navbar d-block d-sm-flex text-center">
                <span class="navbar-text">&copy; BootstrapDash. All rights reserved.</span>
                <div class="navbar-nav ml-auto justify-content-center">
                    <a href="#" class="nav-link">Support</a>
                    <a href="#" class="nav-link">Terms</a>
                    <a href="#" class="nav-link">Privacy</a>
                </div>
            </nav>
        </div>
    </footer>
    <script src="./src/vendors/jquery/dist/jquery.min.js"></script>
    <script src="./src/vendors/popper.js/dist/umd/popper.min.js"></script>
    <script src="./src/vendors/bootstrap/dist/js/bootstrap.min.js"></script>
</body>
</html>
