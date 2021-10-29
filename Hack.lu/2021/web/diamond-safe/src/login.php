<?php
include_once("functions.php");
include_once("config.php");

$_SESSION['CSRFToken'] = md5(random_bytes(32));
if (isset($_SESSION['is_auth']) && $_SESSION['is_auth']){
    redirect('vault.php');
    die();
}

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
                        <li><a href="<?= $base_dir ?>index.php">About</a></li>
                        <li class="active"><a href="<?= $base_dir ?>login.php">Login</a></li>
                    </ul>
                </div>
            </nav>
        </div>
        <div class="container container-body">
<?php
if (isset($_POST['password'])){
    $query = db::prepare("SELECT * FROM `users` where password=sha1(%s)", $_POST['password']);

    if (isset($_POST['name'])){
        $query = db::prepare($query . " and name=%s", $_POST['name']);
    }
    else{
        $query = $query . " and name='default'";
    }
    $query = $query . " limit 1";

    $result = db::commit($query);

    if ($result->num_rows > 0){
        $_SESSION['is_auth'] = True;
        $_SESSION['user_agent'] = $_SERVER['HTTP_USER_AGENT'];
        $_SESSION['ip'] = get_ip();
        $_SESSION['user'] = $result->fetch_row()[1];

        success('Welcome to your vault!');
        redirect('vault.php', 2);
    }
    else{
        error('Wrong login or password.');
    }
}
else{?>
            <div class="panel panel-default">
                <div class="panel-heading">Login</div>
                <div class="panel-body">
                    <form class="form-horizontal" action="<?= $base_dir ?>login.php" method="post">
                        <div class="form-group">
                            <label class="control-label col-sm-2">Login:</label>
                            <div class="col-sm-10">
                                <input class="form-control" name="name" id="name" placeholder="default" value=default disabled>
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="control-label col-sm-2" for="pwd">Password:</label>
                            <div class="col-sm-10">
                                <input type="password" name="password" class="form-control" id="password" placeholder="Enter password">
                            </div>
                        </div>
                        <div class="form-group">
                            <div class="col-sm-offset-2 col-sm-10">
                                <button type="submit" class="btn btn-default">Submit</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
<?php 
}
?>
        <?php print_footer(); ?>

    </body>
</html>