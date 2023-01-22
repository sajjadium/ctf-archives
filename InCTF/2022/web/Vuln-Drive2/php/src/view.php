<?php
include("utils.php");

session_start();
if (!isset($_SESSION['username'])){
    header("Location: /login.php");
    die();
}
$FOLDER = $_SESSION['folder'];
$dirr = ['.','..'];

$files_template  = <<<EOD
<div class="container">
            <div class="container-fluid">
                <ul class="list-group">
                    CONTENT
                  </ul>
            </div>  

        </div>
EOD;


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
        <br><br>
        <div class="container py-3">
            <ul class="nav nav-pills">
                <li class="nav-item">
                    <a class="nav-link active" href="/index.php">index.php</a>
                </li>
            </ul>
        </div>

<?php 
if(isset($_GET['fol'])){
    
    //echo $FOLDER.$_GET['fol'];
    if(check_name($_GET['fol']) && is_dir($FOLDER.$_GET['fol'])){
        $c = "";
        $files = array_diff(scandir($FOLDER.$_GET['fol']),$dirr);
        foreach ($files as $f) {
            
            $c.= "<li class=\"list-group-item\"><a href='/view.php?file=".$_GET['fol']."/".$f."'>$f</a></li>";

        }
        echo str_replace("CONTENT",$c,$files_template);
    }else{
        echo '<div class="alert alert-warning" role="alert">folder not found</div>';
    }
}

if(isset($_GET['file'])){
    $file = $_GET['file'];
    $ext = explode('.', $file);
    $type = substr(strtolower(end($ext)),0,3);
    $file = $FOLDER."/".$file;
    if($type==="txt"){
        try {
            if(file_exists($file)){
                chdir($FOLDER);
                echo file_get_contents($_GET['file']);
            }else{
                echo '<div class="alert alert-warning" role="alert">File not found!</div>';
            }
        } catch (\Throwable $th) {
           echo '<div class="alert alert-warning" role="alert">Some error Occured</div>';
        }
        
    }
    else if($type==="png" || $type==="jpg"){

        try {
            if(file_exists($file)){
                chdir($FOLDER);
                echo "<img src=\"data:image/$type;base64,".base64_encode(file_get_contents($_GET['file']))."\" >";
            }else{
                echo '<div class="alert alert-warning" role="alert">File not found!</div>';
            }
        } catch (Throwable $th) {
            echo '<div class="alert alert-warning" role="alert">Some error Occured</div>';
        }
        
    }
    else{
        echo '<div class="alert alert-warning" role="alert">Invaild type</div>';
    }

}else{
    echo <<<EOD
        <div class="container mt-6">
        <div class="col-md-6">
            <div class="card-body">
                <form autocomplete="off" class="form" role="form" action="/view.php" method="GET" >
                
                    <div class="form-group">
                        <label for="inputPasswordOld">Enter Folder Name</label> 
                        <input class="form-control" name="fol" required="" type="password">
                    </div>
                    
                    <div class="form-group">
                        <button class="btn btn-primary btn-lg float-right"  name="submit" value="something" type="submit">Submit</button>
                    </div>

                </form>
            </div>
        </div>
        </div>
        EOD;
}
?>

</body>
</html>


