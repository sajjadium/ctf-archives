<?php
include "config.php";

if (isset($_POST['but_submit'])) {
    $result = $db_con->prepare('INSERT INTO users (username, password, pic_path) VALUES (:username, :password, \'/var/www/html/avatar/avatar.jpg\')');
    $result->bindValue(':username', $_POST['txt_uname']);
    $result->bindValue(':password', $_POST['txt_pwd']);
    if ($result->execute()) {
        header('location: /index.php');
        exit();
    } else {
        $error = $result->errorInfo()[2];
    }
}
?>
<html>
    <head>
        <title>Penguin (De)Serial Killer</title>
    <style type="text/css">
/* Container */
.container{
    width:40%;
    margin:0 auto;
}

#div_register{
    border: 1px solid gray;
    border-radius: 3px;
    width: 470px;
    height: 270px;
    box-shadow: 0px 2px 2px 0px  gray;
    margin: 0 auto;
}

#div_register h1{
    margin-top: 0px;
    font-weight: normal;
    padding: 10px;
    background-color: cornflowerblue;
    color: white;
    font-family: sans-serif;
}

#div_register div{
    clear: both;
    margin-top: 10px;
    padding: 5px;
}

#div_register .textbox{
    width: 96%;
    padding: 7px;
}

#div_register input[type=submit]{
    padding: 7px;
    width: 100px;
    background-color: lightseagreen;
    border: 0px;
    color: white;
}
</style>
    </head>
    <body>
    <nav>
        <ul>
            <li><a href="/index.php">Login</a></li>
        </ul>
    </nav>

        <div class="container">
        <form method="post" action="">
                <div id="div_register">
                    <h1>Register</h1>
                    <div>
                        <input type="text" class="textbox" id="txt_uname" name="txt_uname" placeholder="Username"/>
                    </div>
                    <div>
                        <input type="password" class="textbox" id="txt_uname" name="txt_pwd" placeholder="Password"/>
                    </div>
                    <div>
                        <input type="submit" value="Submit" name="but_submit" id="but_submit"/>
                    </div>
                    <?php if($error) {echo $error;} ?>
                </div>
            </form>
        </div>
    </body>
</html>
