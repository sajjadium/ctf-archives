<?php
include "config.php";

// Check user login or not
if(!isset($_COOKIE['user'])){
    header('Location: index.php');
}

// logout
if(isset($_POST['logout'])){
    header('Location: index.php');
}

$user_obj = unserialize(base64_decode($_COOKIE['user']));
?>
<!doctype html>
<html>
    <head>
        <title>Penguin (De)Serial Killer</title>
    </head>
    <body>
        <h1>Homepage</h1>
        <?php echo '<img src="data:image/jpeg;base64,' . base64_encode($user_obj->profile_pic) . '">'; ?>
        <form method='post' action="">
            <input type="submit" value="Logout" name="logout">
        </form>
    </body>
</html>
