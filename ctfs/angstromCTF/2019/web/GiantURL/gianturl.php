<?php session_start(); header("Content-Security-Policy: default-src 'self'; style-src 'unsafe-inline';"); ?>
<!doctype html>
<html>
<head>
	<title>GiantURL</title>
</head>
<body style="margin: 0; padding: 0; font-family: sans-serif;">
	<h1 style="font-family: 'Comic Sans MS', sans-serif; background-color: #097aa0; margin-top: 0; padding: 1em; color: white"><span style="color: #b7edff">Giant</span>URL</h1>
	<?php $path = strtok($_SERVER['REQUEST_URI'], '?'); $password = file_get_contents("password"); ?>
	<?php if ($path === '/') : ?>
	<form method="GET" action="/redirect" style="padding-left: 2em;">
		<p>Enter url:</p>
		<input type="hidden" name="_" value="<?php echo base64_encode(hash("sha512", openssl_random_pseudo_bytes(64))); ?>">
		<input type="text" name="url">
		<button type="submit">Lengthen URL</button>
		<input type="hidden" name="__" value="<?php echo base64_encode(hash("sha512", openssl_random_pseudo_bytes(64))); ?>">
	</form><br>
	<form method="POST" action="/report" style="padding-left: 2em;">
		<p>Find a URL you don't think we should be redirecting? Enter the lengthened URL here and an admin will review it:</p>
		<input type="text" name="url">
		<button type="submit">Report URL</button>
	</form>
	<?php elseif ($path === '/redirect') : ?>
	<p style="padding-left: 2em;">Click on <a href=<?php echo htmlspecialchars($_REQUEST['url']); ?>>this link</a> to go to your page!</p>
	<?php elseif ($path === '/report' && $_SERVER['REQUEST_METHOD'] === 'POST') : ?>
	<?php exec('nohup node /app/visit.js '.escapeshellarg($_REQUEST['url']).' > /dev/null 2>&1 &'); ?>
	<p style="padding-left: 2em;">The admin will review the link shortly.</p>
	<?php elseif ($path === '/admin' && $_SERVER['REQUEST_METHOD'] === 'GET') : ?>
	<?php if ($_SESSION['admin'] === 'true') : ?>
		<p style="padding-left: 2em;">Here's your flag: <?php echo getenv('FLAG'); ?></p>
	<?php else : ?>
	<form method="POST" style="padding-left: 2em;">
		<p>Enter password:</p>
		<input type="password" name="password">
		<button type="submit">Log In</button>
	</form>
	<?php endif; ?>
	<?php elseif ($path === '/admin' && $_SERVER['REQUEST_METHOD'] === 'POST') : ?>
	<?php if ($_REQUEST['password'] === $password) : ?>
		<?php $_SESSION["admin"] = "true" ?>
		<p style="padding-left: 2em;">Here's your flag: <?php echo getenv('FLAG'); ?></p>
	<?php else : ?>
		<p style="padding-left: 2em;">Incorrect password.</p>
	<?php endif; ?>
	<?php else : ?>
	<p style="padding-left: 2em;">404 Page not found</p>
	<?php endif; ?>
	<?php
	if ($path === '/admin/changepass' && $_SERVER['REQUEST_METHOD'] === 'POST' && $_SESSION["admin"] === "true") {
		if (strlen($_REQUEST['password']) >= 100 && count(array_unique(str_split($_REQUEST['password']))) > 10) {
			$password = $_REQUEST['password'];
			echo 'Successfully changed password.';
		} else {
			echo 'Password is insecure.';
		}
	}
	file_put_contents("password", $password);
	?>
</body>
</html>
