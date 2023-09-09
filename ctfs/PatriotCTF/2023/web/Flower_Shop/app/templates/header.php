<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Flower Shop</title>
    <link rel="stylesheet" type="text/css" href="public/css/style.css">
</head>
<body>
    <header class="header-banner">
        <div class="banner-left">
            <h1>Flower Shop</h1>
        </div>
        <div class="banner-right">
            <?php
            session_start();

            if (isset($_SESSION['userid'])) {
                echo '<div class="header-banner">';
                echo '<div class="banner-left">';
                echo '</div>';
                echo '<div class="banner-right">';
                echo '<span class="welcome-message">Welcome,</span> <span class="username">' . $_SESSION['username'] . '</span>';
                echo '<a class="logout-button" href="modules/logout.inc.php">Logout</a>';
                echo '</div>';
                echo '</div>';
            }
            ?>
        </div>
    </header>
