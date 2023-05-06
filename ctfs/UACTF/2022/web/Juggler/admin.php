<!DOCTYPE HTML>
<html>
<head>
	<meta charset="utf-8">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css">
	<link rel="stylesheet" href="style.css">
	<title>Juggler - Admin dashboard</title>
</head>

<body>

	<div class="container">

		<h1>Admin dashboard</h1>
		
		<h3>Super secret page only for admin juggler!</h3>
		
		<form autocomplete="off" method="POST">
			<div class="login">
				<label for="username">Username</label>
				<input type="text" name="username"></input>

				<label for="password">Password</label>
				<input type="password" name="password"></input>

				<label for="hmac">HMAC Signature</label>
				<input type="password" name="hmac"></input>
				
				<?php
					$nonce = bin2hex(random_bytes(16));
					echo "<input type=\"hidden\" name=\"nonce\" value=\"{$nonce}\" />";
				?>

				<input type="submit" value="Login"></input>
			</div>
		</form>

		<?php
			include_once('flag.inc.php');

			echo "<p>Challenge nonce: {$nonce}</p>";

			if (!empty($_POST['username']) && !empty($_POST['password']) &&
				!empty($_POST['hmac']) && !empty($_POST['nonce']))
			{
				$secret = hash_hmac('sha256', $_POST['nonce'], $secret);
				$hmac = hash_hmac('sha256', $_POST['username'], $secret);

				if (strcmp($_POST['username'], "admin") == 0 &&
					strcmp($_POST['password'], $password) == 0 &&
					$_POST['hmac'] === $hmac)
					echo "<p style='color:green'>Login successful! Here is your flag: {$flag}</p>";
				else
					echo "<p style='color:red'>Your credentials are incorrect, please try again!</p>";
			}
			elseif ($_SERVER['REQUEST_METHOD'] === 'POST')
			{
				echo "<p style='color:red'>Please enter your credentials and try again!</p>";
			}
		?>
		
		<h4><a href="/">Back to home</a></h4>

	</div>

	<!-- the security on this PHP site is such a joke you could loosely compare it with a whole circus -->
</body>
</html>

