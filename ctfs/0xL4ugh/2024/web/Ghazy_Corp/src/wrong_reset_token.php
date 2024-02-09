<?php
session_start();
require_once("db.php");  
require_once("utils.php");

if(!isset($_GET['email']) || !isset($_SESSION["reset_token3"]))
{
    die("<script>window.location.href='forget_password.php'</script>");
}


//Still Under Development

if(!empty($_GET['email']) && !empty($_GET['token1']) && !empty($_GET['token2']) && !empty($_GET['new_password']))
{
    $email=$_GET['email'];
    $token1=(int)$_GET['token1'];
    $token2=(int)$_GET['token2'];
    if(strlen($_GET['new_password']) < 10)
    {
        die("Plz choose password +10 chars");
    }
    $password=md5($_GET['new_password']);
    if($token1 ===$_SESSION['reset_token3']  &&  $token2 ===$_SESSION['reset_token4']  )
    {
        if ($email=="admin@ghazycorp.com")
        {
            $stmt=$conn->prepare("insert into admins(email,password,level,confirmed) values(?,?,1,1)"); // inserting instead of updating to avoid any conflict.
            $stmt->bind_param("ss", $email,$password);
            if($stmt->execute())
            {
                unset($_SESSION['reset_token3']);
                unset($_SESSION['reset_token4']);
                echo "<script>alert('User Updated Successfully');window.location.href='index.php';</script>";
            }
        }
        else
        {
            $stmt=$conn->prepare("insert into users(email,password,level,confirmed) values(?,?,1,1)"); // inserting instead of updating to avoid any conflict.
            $stmt->bind_param("ss", $email,$password);
            if($stmt->execute())
            {
                echo "<script>alert('User Updated Successfully');window.location.href='index.php';</script>";
            }
        }

    }
    else
    {

        echo "<script>alert('Wrong Token');window.location.href=history.back();</script>";
    }
}
else
{
    echo "please enter email, token1, token2, new_password";
}

?>