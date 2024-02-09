<?php
session_start();
unset($_SESSION['mail_user_id']);

echo "<script>window.location.href='index.php'</script>";
?>