<!DOCTYPE html>
<?php include_once "./includes/config.php"?>
<html lang="en">
	<?php include_once "includes/header.php"?>
    <head>
    <style>
        body {
            background-image: url('/assets/img/peak.png');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
    </style>
    </head>
    <body class="bg-light font-sans antialiased d-flex align-items-center">
    <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <ul class="nav nav-tabs card-header-tabs" id="authTabs">
                                <li class="nav-item">
                                    <a class="nav-link active" id="login-tab" data-toggle="tab" href="#login">Login</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" id="register-tab" data-toggle="tab" href="#register">Register</a>
                                </li>
                            </ul>
                        </div>
                        <div class="card-body tab-content">
                            <div class="tab-pane fade show active" id="login">
                                <h5 class="card-title">Login</h5>
                                <form action="/actions/login.php" method="post">
                                    <div class="form-group">
                                        <label for="username">Username</label>
                                        <input type="text" class="form-control" id="username" name="username" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="password">Password</label>
                                        <input type="password" class="form-control" id="password" name="password" required>
                                    </div>
                                    <br>
                                    <button type="submit" name="button" class="btn btn-primary">Login</button>
                                </form>
                            </div>
                            
                            <div class="tab-pane fade" id="register">
                                <h5 class="card-title">Register</h5>
                                <form action="/actions/register.php" method="post">
                                    <div class="form-group">
                                        <label for="username">Username</label>
                                        <input type="text" class="form-control" id="username" name="username" required>
                                    </div>
                                    <div class="form-group">
                                        <label for="password">Password</label>
                                        <input type="password" class="form-control" id="password" name="password" required>
                                    </div>
                                    <br>
                                    <button type="submit" name="button" class="btn btn-success">Register</button>
                                </form>
                            </div>
                        </div>
                        <?php include "includes/error.php";?>
                    </div>
                </div>
            </div>
        </div>
        <script>
            // JavaScript to handle tab switching
            $(document).ready(function() {
                $('#authTabs a').on('click', function(e) {
                    e.preventDefault();
                    $(this).tab('show');
                });
            });
        </script>
	</body>
</html>