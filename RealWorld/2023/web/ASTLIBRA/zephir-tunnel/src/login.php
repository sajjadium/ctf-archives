<?php
require_once('config.php');
if(isset($_POST['username']) && isset($_POST['password'])){
    $username = $_POST['username'];
    $password = $_POST['password'];
    $query = "SELECT * FROM users WHERE username = ? AND password = ?";
    $stmt = $dbc->prepare($query);
    $stmt->bind_param("ss", $username, $password);
    $stmt->execute();
    $result = $stmt->get_result();
    if($result->num_rows > 0){
        $row = $result->fetch_assoc();
        $_SESSION['username'] = $row['username'];
        header('Location: index.php');
    }else{
        die("Invalid username or password");
    }
}

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="shortcut icon" href="assets/images/favicon.ico" type="image/x-icon">
    <title>Login</title>

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
            <h3 class="text-center text-white font-weight-light mb-4">LOG IN</h3>
            <form action="login.php" method="POST">
                <div class="form-group">
                    <input type="text" name="username" placeholder="Username" class="form-control">
                </div>
                <div class="form-group">
                    <input type="text" name="password" placeholder="Password" class="form-control">
                </div>
                <input type="submit" value="Login" class="btn btn-danger btn-block mb-3">
            </form>
            <div class="d-flex justify-content-between mt-4">
                <a class="text-white text-center font-weight-light" href="register.php">Register</a>
        
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
