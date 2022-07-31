<!DOCTYPE html>
<html>
  <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <title>Picture Frame Generator</title>
    <style>
      #frame {
        position:relative;
        top:0px;
        left:0px;
        width:564px;
        height:686px;
        background-image: url(frame-1.png);
        background-position: center;
        background-size: cover;
      }
      #submission {
        position:absolute;
        width:244px;
        height:376px;
        object-fit: cover;
        left: 0;
        top: 0;
        right: 0;
        bottom: 0;
        display: block;
        margin: auto;
      }
    </style>
  </head>
  <body>
    <div class="container text-center">
      <div class="row">
        <div class="col py-3">
          <h1>Picture Frame Generator</h1>
        </div>
      </div>
      <div class="row">
        <div class="col">
          <form action="/" method="post" enctype="multipart/form-data">
            Select image to upload:
            <input type="file" name="fileToUpload" id="fileToUpload">
            <input type="submit" value="Upload Image" name="submit">
          </form>
        </div>
      </div>
      <div class="row justify-content-center">
<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
          if (isset($_POST["submit"])) {
            $allowed_extensions = array(".jpg", ".jpeg", ".png", ".gif");
            $filename = $_FILES["fileToUpload"]["name"];
            $tmpname = $_FILES["fileToUpload"]["tmp_name"];
            $target_file = "uploads/" . bin2hex(random_bytes(8)) . "-" .basename($filename);

            $has_extension = false;
            foreach ($allowed_extensions as $extension) {
              if (strpos(strtolower($filename), $extension) !== false) {
                $has_extension = true;
              }
            }
            
            if ($_FILES["fileToUpload"]["size"] < 2000000) {
              if (getimagesize($tmpname) && $has_extension) {
                if (move_uploaded_file($tmpname, $target_file)) {     
                  echo "<div id='frame'><img src='$target_file' alt='Your image failed to load :(' id='submission'></div>";
                } else {
                  echo "There was an error uploading your file. Please contact an admin.";
                }
              } else {
                echo "Your picture is not a picture and could not be framed.";
              }
            } else {
              echo "Your picture is too large for us to process.";
            }
          }
        ?>
      </div>
    </div>
  </body>
</html>
