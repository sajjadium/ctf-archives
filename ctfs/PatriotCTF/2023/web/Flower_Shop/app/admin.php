<?php

session_start();

if (!isset($_SESSION['userid'])) {
    header("Location: login.php?error=notloggedin");
    exit();
} 

if ($_SESSION['username'] !== "admin" ) {
    header("Location: login.php?error=notadmin");
    exit();
}

?>

<?php include "templates/header.php"; ?>    
    <div class="container">
        <h3>CACI{FAKE_FLAG_FOR_TESTING}</h3>
    </div>
<?php include "templates/footer.php"; ?>
