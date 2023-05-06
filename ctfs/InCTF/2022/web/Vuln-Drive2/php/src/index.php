<?php
include("utils.php");

session_start();


if (!isset($_SESSION['username'])){
    header("Location: /login.php");
    die();
}

$FOLDER = $_SESSION['folder'];




//create new folder inside uploads using get parameter
if (isset($_GET['new'])) {
    if(check_name($_GET["new"])){
        $newfolder = $FOLDER.$_GET['new'];
        if (!file_exists($newfolder)) {
            
            mkdir($newfolder);
        }else{
            $error = "folder already exist";
        }
    }else{
        die('not allowed');
    }
}

#file upload
if(isset($_POST["submit"])){
    if(isset($_FILES['file'])&& isset($_POST['path'])){
        if(!check_name($_POST["path"])){
            die("not allowed");
        }
        $file = $_FILES['file'];
        $fileName = $file['name'];
        $fileSize = $file['size'];
        $fileError = $file['error'];
        $fileExt = explode('.', $fileName);
        $fileActualExt = strtolower(end($fileExt));
        if($fileError === 0){
            if($fileSize < 100000){
                $name = uniqid('', true).".".$fileActualExt;
                $fileDestination = $FOLDER.$_POST['path'];
                upload($file['tmp_name'], $fileDestination,$name);
                header("Location: index.php?uploadsuccess");
            }else{
                $error =  "Your file is too big!";
            }
        }else{
            $error =  "There was an error uploading your file!";
        }
        
    }else{
        $error =  "parameter missing";
    }
}




?>

<html>
    <head>
        <title>Index</title>
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
            <ul class="nav nav-pills">
                <li class="nav-item">
                    <a class="nav-link active" href="/view.php">view</a>
                </li>
            </ul>
             <div class="row">
            <div class="col-md-12"> 
            <div class="row justify-content-center">
                <div class="col-md-6">
            
            <hr class="mb-5">
            <div class="card card-outline-secondary">
                <div class="card-header">
                    <h3 class="mb-0">Create New Folder</h3>
                  </div>
                <div class="card-body">
                    <form autocomplete="off" class="form" role="form" action="/index.php" method="GET" >
                      
                        <div class="form-group">
                            <label for="inputPasswordOld">Enter Folder Name</label> 
                            <input class="form-control" name="new" required=""  type="text">
                        </div>
                        
                        <div class="form-group">
                            <button class="btn btn-primary btn-lg float-right"  value="Upload" name="submit" type="submit">Submit</button>
                        </div>

                    </form>
                  </div>
                  <hr>
                  <br>
                  <br>

              <div class="card-header">
                <h3 class="mb-0">Upload you files</h3>
              </div>
              <div class="card-body">
                <form autocomplete="off" class="form" role="form" action="/index.php" method="post" enctype="multipart/form-data">
                    <div class="form-group">
                        <div class="mb-3">
                            <label for="formFile" class="form-label">Select file to submmit</label>
                            <input class="form-control" name="file" type="file" id="formFile">
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="inputPasswordOld">Enter Folder Name To upload</label> 
                        <input class="form-control" name="path" required="" type="password">
                    </div>

                    <div class="form-group">
                        <button class="btn btn-success btn-lg float-right" name="submit"  value="Upload" type="submit">Submit</button>
                    </div>
                </form>  
              </div>
            </div>
            <!-- /form card change password -->
        <?php if(isset($error)) {
            echo '<div class="alert alert-warning" role="alert">';
                echo $error;
             echo  "</div>";
         
         } ?>
         </div>
        </div>
        </div>
        </div>
        </div>
    

    </body>
</html>


