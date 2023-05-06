<?php function make_header($main_class) { ?>
<?php global $nonce; ?>
<html>
<head>
	<link rel="stylesheet" href="/css/style.css" nonce="<?php echo $nonce; ?>" />
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Boogaloo" nonce="<?php echo $nonce; ?>" />
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bangers" nonce="<?php echo $nonce; ?>" />
	<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js" nonce="<?php echo $nonce; ?>"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/lettering.js/0.7.0/jquery.lettering.min.js" nonce="<?php echo $nonce; ?>"></script>
	<script src="https://www.google.com/recaptcha/api.js?render=6LejJMscAAAAAH38ZmF1iIpcKD94XjjGqJzidaYu" nonce="<?php echo $nonce; ?>"></script>
	<script src="/js/main.js" nonce="<?php echo $nonce; ?>"></script>
</head>
<body>
<header>
	<a href="/"><div class="site-title">HQB Comic Library Catalog<sub>beta</sub></div></a>
	<?php if (isset($_SESSION["user"]) && $_SESSION["user"]["is_admin"]) { ?>
		<a href="/admin.php"><div class="nav">Administration</div></a>
	<?php } ?>
	<?php if (isset($_SESSION["user"])) { ?>
		<a href="/self.php"><div class="nav">Your Issues</div></a>
		<a href="/edit.php"><div class="nav">Add a New Issue</div></a>
	<?php } ?>
	<div class="nav login">
		<?php if (isset($_SESSION["user"])) { ?>
			<div class="message">Hi, <?php echo $_SESSION["user"]["username"]; ?></div>
			<div class="dropdown">
				<form action="/user.php" method="POST">
					<button name="action" value="logout">Log Out</button>
				</form>
			</div>
		<?php } else { ?>
			<div class="message">Log In or Register</div>
			<div class="dropdown">
				<form action="/user.php" method="POST">
					<input type="text" name="username" placeholder="Username" />
					<input type="password" name="password" placeholder="Password" />
					<button name="action" value="login">Log In</button>
					<button name="action" value="register">Register</button>
				</form>
			</div>
		<?php } ?>
	</div>
</header>
<?php if (isset($_SESSION["flash"])) { ?>
	<div class="messages">
		<?php foreach ($_SESSION["flash"] as $message) { ?>
			<div class="message <?php echo $message["severity"]; ?>">
				<?php echo $message["content"]; ?>
			</div>
		<?php } ?>
	</div>
<?php unset($_SESSION["flash"]); ?>
<?php } ?>
<main class="<?php echo $main_class; ?>">
<?php } ?>
