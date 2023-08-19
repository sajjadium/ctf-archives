<?php
    include_once("../config.php");
    include_once("admin_auth_service.php");
    session_start();
    
    if($_SESSION["username"] != "admin")
        die("you are not admin");
    
    $password = file_get_contents('/flag', true);
    request_resetpassword($AUTH_SERVER, $_SESSION["access_token"], $_SESSION["uid"], $password);
    echo "<script>alert('password reset!'); window.location.href = '/admin/index.php'; </script>"; 
?>