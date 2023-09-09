<?php

session_start();

include __DIR__ . "/classes/dbh.php";
include __DIR__ . "/modules/helpers.php";

$_SESSION['token'] = createCsrf();

?>

<?php include "templates/header.php"; ?>
    <div class="container">
        <section class="index-login">
            <div class="index-login-signup">
                <h4>SIGN UP</h4>
                <p>Please go to <a href="https://webhook.site/">https://webhook.site/</a> to get your own unique webhook URL. This will be used for password resets.</p>
                <form action="modules/signup.inc.php" method="post">
                    <input type="text" name="uid" placeholder="Username">
                    <input type="password" name="pwd" placeholder="Password">
                    <input type="text" name="wh" placeholder="Webhook">
                    <button type="submit" name="submit">SIGN UP</button>
                </form>
            </div>
			<hr>
            <div class="index-login-login">
                <h4>LOGIN</h4>
                <form action="modules/login.inc.php" method="post">
                    <input type="text" name="uid" placeholder="Username">
                    <input type="password" name="pwd" placeholder="Password">
                    <button type="submit" name="submit">LOG IN</button>
                </form>
            </div>
			<hr>
            <div class="index-login-reset">
                <h4>PASSWORD RESET</h4>
                <form action="modules/reset.inc.php" method="post">
                    <input type="text" name="uid" placeholder="Username">
                    <input type="hidden" name="token" value="<?php echo $_SESSION['token'] ?>">
                    <button type="submit" name="submit">RESET PASSWORD</button>
                </form>
            </div>
        </section>
    </div>
	<script src="public/js/alert.js"></script>
<?php include "templates/footer.php"; ?>
