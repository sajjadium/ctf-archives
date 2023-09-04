<?php
	if(!defined('__MAIN__')) exit('!^_^!');
?>
<html>
	<head>
		<meta charset="UTF-8">
		<title>WACON CMS</title>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
		<script src="./static/javascript/main.js"></script>
		<style>
			.bd-placeholder-img {
				font-size: 1.125rem;
				text-anchor: middle;
				-webkit-user-select: none;
				-moz-user-select: none;
				-ms-user-select: none;
				user-select: none;
			}

			@media (min-width: 768px) {
				.bd-placeholder-img-lg {
					font-size: 3.5rem;
				}
			}
			/* Show it's not fixed to the top */
			body {
				min-height: 75rem;
			}
		</style>
	</head>
	<body>
		<nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
			<a class="navbar-brand" href="./">WACON CMS</a>
			<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
				<span class="navbar-toggler-icon"></span>
			</button>
			<div class="collapse navbar-collapse" id="navbarCollapse">
				<?php if(is_login()) { ?>
				<ul class="navbar-nav mr-auto">
					<li class="nav-item">
						<a class="nav-link" href="./board.php">Board</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="./myinfo.php">Myinfo</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="./note.php">Note</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="./logout.php">Logout</a>
					</li>
				</ul>
				<?php }else { ?>
				<ul class="navbar-nav mr-auto">
					<li class="nav-item">
						<a class="nav-link" href="./login.php">Login</a>
					</li>
					<li class="nav-item">
						<a class="nav-link" href="./register.php">Register</a>
					</li>
				</ul>
				<?php } ?>
			</div>
		</nav>
