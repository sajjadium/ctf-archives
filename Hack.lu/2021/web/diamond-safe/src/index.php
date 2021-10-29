<?php
include_once("functions.php");
include_once("config.php");
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Diamond Safe</title>
        <meta charset="utf-8">
        <script src="<?= $static_dir ?>jquery-3.2.1.min.js"></script>
        <script src="<?= $static_dir ?>bootstrap.min.js"></script>
        <link rel="stylesheet" href="<?= $static_dir ?>bootstrap.min.css">
        <link rel="stylesheet" href="<?= $static_dir ?>main.css">
        <link rel="icon" type="image/png" href="<?= $static_dir ?>favicon.png">
    </head>
    <body>
        <div class="container">
            <br>
            <nav class="navbar navbar-default navbar">
                <div class="container-fluid">
                    <div class="navbar-header">
                        <a class="navbar-brand">Diamond Safe</a>
                    </div>
                    <ul class="nav navbar-nav">
                        <li class="active"><a href="<?= $base_dir ?>index.php">About</a></li>
                        <li><a href="<?= $base_dir ?>vault.php">My Vault</a></li>
                    </ul>
                </div>
            </nav>
        </div>
        <div class="container container-body">
            <div class="panel panel-default">
                <div class="panel-heading">About</div>
                <div class="panel-body">
                    <img src="<?= $img_dir ?>logo.png" class="img-responsive">
                </div>
            </div>
            <?php print_footer(); ?>
            
        </div>
    </body>
</html>