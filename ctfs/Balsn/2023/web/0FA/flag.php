<?php
include_once("config.php");
fingerprint_check();
if(!isset($_POST['username']) || $_POST['username'] !== "admin")
    die("Login failed!");
?>
<html>
<head>
    <title>Balsn CTF 2023 - 0FA</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
</head>
<body>
  Here is your flag: <?php echo $flag; ?>
</body>
</html>