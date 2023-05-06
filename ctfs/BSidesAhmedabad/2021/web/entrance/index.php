<?php
session_start();

if (empty($_SESSION['login'])) {
    header("Location: /login.php");
    exit();
}
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Entrance</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/uikit@3.7.6/dist/css/uikit.min.css" />
        <script src="https://cdn.jsdelivr.net/npm/uikit@3.7.6/dist/js/uikit.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/uikit@3.7.6/dist/js/uikit-icons.min.js"></script>
    </head>
    <body class="uk-container">
	      <div class="uk-width-1-1">
		        <div class="uk-container">
                <div class="uk-card uk-card-default uk-card-body">
                    <h3 class="uk-card-title">Welcome</h3>
                    <?php if ($_SESSION['privilege'] == "admin") { ?>
                        <p><?php echo file_get_contents("/flag.txt"); ?></p>
                    <?php } else { ?>
                        <p>Welcome, guest!</p>
                    <?php } ?>
                </div>
            </div>
        </div>
    </body>
</html>
