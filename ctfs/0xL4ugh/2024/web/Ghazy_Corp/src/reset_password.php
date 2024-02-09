<?php
session_start();
require_once("db.php");
require_once("utils.php");

if(!empty($_SESSION['reset_token1']) && !empty($_SESSION['reset_email']))
{
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
        if($token1 === $_SESSION['reset_token1'] && $token2===$_SESSION['reset_token2'] && $email===$_SESSION['reset_email'])
        {

            $uuid=guidv4();
            $stmt=$conn->prepare("insert into admins(email,password,level,confirmed) values(?,?,1,1)"); // inserting instead of updating to avoid any conflict.
            $stmt->bind_param("ss",$email,$password);
            if($stmt->execute())
            {
                unset($_SESSION['reset_email']);
                unset($_SESSION['reset_token1']);
                unset($_SESSION['reset_token2']);
                echo "<script>alert('User Updated Successfully');window.location.href='index.php';</script>";
            }

        }
        else
        {
            unset($_SESSION['reset_token1']);
            unset($_SESSION['reset_token2']);
            // to be implemented : send mail with the new tokens
            echo "<script>alert('Wrong Token');window.location.href='wrong_reset_token.php?email=$email';</script>";
        }
    }
    else
    {
        echo "please enter email,token,new_password";
    }
}
else
{
    die("<script>window.location.href='forget_password.php'</script>");
}

?>