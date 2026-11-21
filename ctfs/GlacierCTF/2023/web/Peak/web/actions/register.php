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
            $hashedPassword = password_hash($password, PASSWORD_DEFAULT);

            $sql = $pdo->prepare("INSERT INTO users (username, password) VALUES (:username, :password)");
            $sql->bindParam(':username', $username, PDO::PARAM_STR);
            $sql->bindParam(':password', $hashedPassword, PDO::PARAM_STR);

            try 
            {
                $sql->execute();

                $sql = $pdo->prepare("SELECT * FROM users WHERE username=:name");
                $sql->bindValue(':name', $username);
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
                    header('Location: /');
                }
            } 
            catch (PDOException $e) 
            {
                throw new Exception("Could not register with this username! Try again with a different name.");
            }
        }
    }
}
catch(Exception $ex)
{
    $_SESSION['error'] = htmlentities($ex->getMessage());
    header('Location: /login.php');
}
?>