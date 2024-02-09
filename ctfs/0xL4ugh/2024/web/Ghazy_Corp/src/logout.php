<?php
session_start();
unset($_SESSION['user_id']);
unset($_SESSION['role']);
unset($_SESSION["email"]);
unset($_SESSION["confirmed"]);

echo "<script>window.location.href='index.php'</script>";
?>