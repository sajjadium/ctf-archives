<?php
    error_reporting(E_ERROR | E_PARSE);
    require_once('private/jwt.php');
    require_once('private/mysql.php');

    function custom_handler($exception){
        echo $exception;
    }
    set_exception_handler('custom_handler');


    if($_SERVER['REQUEST_METHOD'] == 'POST'){
        $jwt = $_COOKIE['AUTHKEY'];
        $uname = $_POST['username'];
        $psw = $_POST['password'];

        try{
            if(isset($_POST['username']) && isset($_POST['password'])){
                $sql = new MySQLobject();
                if(!$sql->verify_login($uname, $psw)){
                    die('{"error":"wrong username or password"}');
                }else{
                    $jwt = generate_jwt($uname, $psw);
                    set_jwt($jwt);
                    header('Location: http://'.$_SERVER['HTTP_HOST'].'/account.php?name='.$_POST["username"]);
                }
            }
        }catch(Exception $error){
            die($error->getMessage());
        }
        if($jwt != ""){
            die('{"Success":"'.$jwt.'"}');
        }
        die('{"error":""}');
    }

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <meta http-equiv="Content-Security-Policy" content="default-src 'self' data: *; connect-src 'self'; object-src 'none';">
    <title>ColorGram</title>
</head>
<body class="container-fluid m-0 p-0">
    <?php include('assets/navbar.php');?>
    <div class="row container-fluid justify-content-center">
        <div class="col-12 justify-content-center">
            <h1 class="text-center fs-1 text-decoration-underline my-5 fw-bold">Login to your account!</h1>
        </div>
    </div>
    <div class="row container-fluid justify-content-center">
        <div class="col-6 justify-content-center">
            <form class="mt-4" action='login.php' method='POST'>
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" name="username" class="form-control" id="username">
                </div>
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" name="password" class="form-control" id="password">
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
              </form>
        </div>
    </div>
</body>
</html>
