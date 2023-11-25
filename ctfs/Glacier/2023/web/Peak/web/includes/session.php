<?php

include_once "config.php";

if(isset($_SESSION['user']))
{
    $sql = $pdo->prepare("SELECT * FROM users WHERE id=:id");
    $sql->bindValue(':id', $_SESSION['user']['id']);
    $sql->execute();
    $user = $sql->fetch();
    
    if ($user)
    {
        $id = $user["id"];
        $username = $user["username"];
        $role = $user["role"];
        $_SESSION['user'] = array();
        $_SESSION['user']['id'] = $id;
        $_SESSION['user']['username'] = $username;
        $_SESSION['user']['role'] = $role;
    }
    else
    {
        session_destroy();
        header('Location: /');
        return;
    }
}
?>