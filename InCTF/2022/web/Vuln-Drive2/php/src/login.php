<?php
session_start();
if (!file_exists('uploads')) {
    mkdir('uploads');
}

if(isset($_POST['submit'])){
    if(isset($_POST['username'])){
        $_SESSION["username"] = $_POST["username"];
        $folder = './uploads/'.session_id()."/";
        if (!file_exists($folder)) {
          mkdir($folder);
        }  
        $_SESSION['folder'] = $folder;
        header("Location: /index.php");
        die();

    }else{
        echo "no username provided";
    }
}

?>

<html>
    <head>
        <title>Login</title>
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
        <style>
            body {
                margin: 0;
                background-color: #ecfab6;
            }
            /* Scroll to Top */
            #scroll-to-top {
            cursor: pointer;
            position: fixed;
            bottom: 20px;
            right: 20px;
            display: none;
            }
        </style>
    </head>
    <body>
        
            
            <div class="container py-3">
             <div class="row">
            <div class="col-md-12"> 
            <div class="row justify-content-center">
                <div class="col-md-6">
            
            <hr class="mb-5">
            <div class="card card-outline-secondary">
              <div class="card-header">
                <h3 class="mb-0">login</h3>
              </div>
              <div class="card-body">
                <form autocomplete="off" class="form" role="form" method="POST" action="/login.php">
                  <div class="form-group">
                    <label for="inputPasswordOld">Username</label> 
										<input class="form-control"  name="username"  required="" type="text">
                  </div>
                  
                  <div class="form-group">
                    <button class="btn btn-success btn-lg float-right" type="submit" name="submit" value="submit">Submit</button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
        </div>
        </div>
        </div>
    

    </body>
</html>


