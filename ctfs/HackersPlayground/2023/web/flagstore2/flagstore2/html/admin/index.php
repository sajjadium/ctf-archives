<?php
    session_start();
    if($_SESSION["username"] != "admin")
        die("you are not admin");
?>
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Flag Store v2</title>
  </head>
  <body>
    <h1>Admin page</h1>
    <a href="/admin/reset.php">[reset password] </a>
  </body>
</html>
