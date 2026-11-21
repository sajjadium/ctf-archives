<?php
include_once "../includes/session.php";

try
{
    if($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST['username']) && isset($_POST['password']))
    {
      $username = $_POST['username'];
      $password = $_POST['password'];

      if ($username !== "" && $password !== "")
      {
        $sql = $pdo->prepare("SELECT * FROM users WHERE username=:name");
        $sql->bindValue(':name', $username);
        $sql->execute();
        $user = $sql->fetch();
        
        if ($user)
        {
          $id = $user["id"];
          $username = $user["username"];
          $role = $user["role"];

          if(password_verify($password, $user["password"]))
          {
            $_SESSION['user'] = array();
            $_SESSION['user']['id'] = $id;
            $_SESSION['user']['username'] = $username;
            $_SESSION['user']['role'] = $role;
            header('Location: /');
          }
          else 
          {
            throw new Exception("Invalid username or password!");
          }
        }
        else 
        {
          throw new Exception("Invalid username or password!");
        }
      }
      else 
      {
        throw new Exception("Username and Password required!");
      }
    }
}
catch(Exception $ex)
{
    $_SESSION['error'] = htmlentities($ex->getMessage());
    header('Location: /login.php');
}
?>