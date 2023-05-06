<?php
	error_reporting(0);
	session_start();

	if (!in_array($_SERVER['HTTP_X_REAL_IP'], ['127.0.0.1', gethostbyname('proxy'), gethostname('prerender')]))
	{
		header('HTTP/1.0 403 Forbidden');
		die('<h1>Forbidden</h1><p>Only admins allowed to login.</p>');
	}
?>

<!DOCTYPE html>
<html lang="en">
	<body>
		<div>
			<p> Welcome back, admin! <p>
			<p> Here's your cereal. </p>
			<img src="images/cereal.jpg" alt="Cereal" width="200" height="200">
			<p> And your flag: <?php echo getenv("FLAG"); ?> </p>
		</div>
	</body>
</html>
