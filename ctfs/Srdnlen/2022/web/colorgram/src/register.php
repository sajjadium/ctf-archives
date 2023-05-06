<?php
    error_reporting(E_ERROR | E_PARSE);
    require_once('private/jwt.php');
    require_once('private/mysql.php');
    require_once('private/filters.php');

    function custom_handler($exception){
        echo $exception;
    }
    set_exception_handler('custom_handler');

    if($_SERVER['REQUEST_METHOD'] == 'POST'){
        if(isset($_POST['username']) && isset($_POST['password']) && isset($_POST['email']) && isset($_POST['description'])){
            $uname = validate_username($_POST['username']);
            $psw = validate_password($_POST['password']);
            $email = validate_email($_POST['email']);
            $desc = validate_description($_POST['description']);
            try{
                $sql = new MySQLobject();
                $sql->register($uname, $email, $psw, $desc);

                $jwt = generate_jwt($uname, $psw);
                set_jwt($jwt);
            }catch(Exception $error){
                die('{"error":"unable to register your account"}');
            }
            header('Location: http://'.$_SERVER['HTTP_HOST'].'/account.php?name='.$uname);

        }else{
            die('{"error":"Invalid input!"}');
        }
        die('{"Success":"'.$jwt.'"}');
    }

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8" crossorigin="anonymous"></script>
    <meta http-equiv="Content-Security-Policy" content="default-src 'self' data: *; connect-src 'self'; object-src 'none';">
    <title>ColorGram</title>
</head>
<body class="container-fluid m-0 p-0">
    <?php include('assets/navbar.php');?>
    <div class="row container-fluid justify-content-center">
        <div class="col-12 justify-content-center">
            <h1 class="text-center fs-1 text-decoration-underline my-5 fw-bold">Register your new account!</h1>
        </div>
    </div>
    <div class="row container-fluid justify-content-center">
        <div class="col-6 justify-content-center">
            <form class="mt-4" action='register.php' method='POST'>
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" name="username" class="form-control" id="username">
                </div>
                <div class="mb-3">
                  <label for="email" class="form-label">Email address</label>
                  <input type="email" name="email" class="form-control" id="email">
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" name="password" class="form-control" id="password">
                </div>
                <div class="form-floating mb-3">
                    <textarea class="form-control" name="description" placeholder="Write your description here" id="description" style="height:100px;"></textarea>
                    <label for="description">Description</label>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
              </form>
        </div>
    </div>
</body>
</html>
