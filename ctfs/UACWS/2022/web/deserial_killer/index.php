<?php
include "config.php";

if (isset($_POST['but_submit'])) {
    $result = $db_con->prepare('SELECT * FROM users WHERE username = :username AND password = :password');
    $result->bindValue(':username', $_POST['txt_uname']);
    $result->bindValue(':password', $_POST['txt_pwd']);
    $result->execute();

    if ($result) {
        $row = $result->fetch();
        if ($row) {
            $tmp = base64_encode(serialize(new User($row['username'], $row['pic_path'])));
            setcookie("user", $tmp);
            header('location: /home.php');
            exit;
        } else {
            $failed = 'Login failed! Invalid credentials!';
        }
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

/* Login */
#div_login{
    border: 1px solid gray;
    border-radius: 3px;
    width: 470px;
    height: 270px;
    box-shadow: 0px 2px 2px 0px  gray;
    margin: 0 auto;
}

#div_login h1{
    margin-top: 0px;
    font-weight: normal;
    padding: 10px;
    background-color: cornflowerblue;
    color: white;
    font-family: sans-serif;
}

#div_login div{
    clear: both;
    margin-top: 10px;
    padding: 5px;
}

#div_login .textbox{
    width: 96%;
    padding: 7px;
}

#div_login input[type=submit]{
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
        <li><a href="/register.php">Register</a></li>
    </ul>
    </nav>
       <div class="container">
        <form method="post" action="">
                <div id="div_login">
                    <h1>Login</h1>
                    <div>
                        <input type="text" class="textbox" id="txt_uname" name="txt_uname" placeholder="Username" />
                    </div>
                    <div>
                        <input type="password" class="textbox" id="txt_uname" name="txt_pwd" placeholder="Password"/>
                    </div>
                    <div>
                        <input type="submit" value="Submit" name="but_submit" id="but_submit" />
                    </div>
                    <?php if ($failed) { echo $failed;} ?>
                </div>
            </form>
        </div>
    </body>
</html>
