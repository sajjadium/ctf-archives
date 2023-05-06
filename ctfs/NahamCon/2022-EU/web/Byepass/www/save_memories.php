<?php
error_reporting(E_ALL);
ini_set('display_errors',1);

$target_dir = "/var/www/html/uploads/";
$uploadOk = 1;

$ext_denylist = array(
    "php",
    "php2",
    "php3",
    "php4",
    "php5",
    "php6",
    "php7",
    "phps",
    "phps",
    "pht",
    "phtm",
    "phtml",
    "pgif",
    "shtml",
    "phar",
    "inc",
    "hphp",
    "ctp",
);

if(isset($_POST["submit"])) {    
    $target_file = basename($_FILES["fileToUpload"]["name"]);
    $filename = $_FILES["fileToUpload"]["name"];
    $uploadOk = 1;
    if ($filename== ""){
        echo("<br><br><br><br><h1>ERROR:</h1> No file was supplied.");
        $uploadOk = 0;
    }

    $ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
    if ( in_array($ext, $ext_denylist)) {
        echo('<br><br><br><br><h1>ERROR:</h1> Not a valid image to upload');
        $uploadOk = 0;
    }

    if ($_FILES["fileToUpload"]["size"] > 500000) {
      echo("<br><br><br><br><h1>ERROR:</h1> This file is too large for us to store!");
      $uploadOk = 0;
    }

    if ($uploadOk){

        $moved = move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);
        if ($moved){
            echo("<br><br><br><br><h1>SUCCESS:</h1> Your memory has been saved, you can view your photographs here: <a href='$filename'>/uploads/$filename</a>.");
        } else {
            echo("<br><br><br><br><h1>ERROR:</h1> Sorry, there was an error uploading your file '$filename'.<br><br>");
            echo($_FILES['fileToUpload']['error']);
            var_dump($_FILES);
        }
    }
}

?>


<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>Say GoodBye</title>
        <!-- Font Awesome icons (free version)-->
        <script src="https://use.fontawesome.com/releases/v6.1.0/js/all.js" crossorigin="anonymous"></script>
        <!-- Google fonts-->
        <link href="https://fonts.googleapis.com/css?family=Catamaran:100,200,300,400,500,600,700,800,900" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css?family=Lato:100,100i,300,300i,400,400i,700,700i,900,900i" rel="stylesheet" />
        <!-- Core theme CSS (includes Bootstrap)-->
        <link href="css/styles.css" rel="stylesheet" />
    </head>
    <body id="page-top">
        <!-- Navigation-->
        <nav class="navbar navbar-expand-lg navbar-dark navbar-custom fixed-top">
            <div class="container px-5">
                <a class="navbar-brand" href="index.php">Say GoodBye</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item"><a class="nav-link" href="save_memories.php">START SAVING MEMORIES</a></li>
                    </ul>
                </div>
            </div>
        </nav>
        <section id="scroll">
            <br><br><br><br>
            <div class="container px-5">
                <div class="row gx-5 align-items-center">
                    <div class="col-lg-6 order-lg-2">
                        <br><br><br><br><br><br><br><br><br><br>
                    <form method="post" enctype="multipart/form-data">
                    <div class="frame">
                        <div class="center">
                            <div class="title">
                                <h2>Drop file to upload</h2>
                            </div>
                                <div class="dropzone">
                                    <img src="http://100dayscss.com/codepen/upload.svg" class="upload-icon" />
                                    <input type="file" class="upload-input" name="fileToUpload" />
                                </div>
                                <button type="button" class="uploadbtn"><input type="submit" name="submit">Upload file</button>
                        </div>
                    </div>
                    </form>
                    </div>
                    <div class="col-lg-6 order-lg-1">
                        <div class="p-5">
                            <h2 class="display-4">Save Memories</h2>
                            <p>
                                Upload your favorite pictures of you and your loved ones!
                            </p>
                            <p>
                                <b>For better security, we limit file extensions that could compromise our service.</b>
                            </p>
                            
                            <!-- original pen: https://codepen.io/roydigerhund/pen/ZQdbeN  -->
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
</html>