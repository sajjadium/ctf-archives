<?php
session_start();
if (!isset($_SESSION["username"])) {
	header("Location: login.php");
	exit(1);
}
if ($_SERVER["REQUEST_METHOD"] === "POST") {
	if (!isset($_POST["bname"]) || !isset($_POST["blog"]))
		die('Blog\'s name or Blog\'s Content is not set.');
	require("db/config.php");
	require("class.php");

		$id = sha1(time());
		$req = bin2hex(random_bytes(16));

	if (!($blog = $conn->prepare("INSERT INTO Blog_posts1 (name, poster, content) VALUES (?, ?, ?)")))
		die('Error creating your post.');
	if (!($blog->bind_param("sss", $req, $_SESSION["username"],$_POST['blog'])) || !($blog->execute())){
		echo $blog->error;
		die('Error creating your post.');
	}
	$blog->close();
	$conn->close();
	$ser=new posts($req);
	$token=base64_encode(serialize($ser));
	header("Location: view/posts.php?token=".$token);
}
?>
<!DOCTYPE>
<html>
<head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Blog</title>
        <link rel="stylesheet" type="text/css" href="./css/styles.css" />
</head>
<body>
	<div class="nav-top">
		<ul class="points">
			<li style="border-right: 1px solid white; background-color: #ff2600"><a href="index.php">Blog</a></li>
			<li><a href="view/posts.php">Posts</a></li>
		</ul>
	</div>
	<div class="main">
		<form method="POST">
			<div class="ftags">
				<input style="text-align: center; width: 300px;" class="in" name="bname" placeholder="Blog Name" />
			</div>
			<div class="ftags">
				<textarea class="in" type="text" name="blog" placeholder="..."></textarea>
			</div>
			<div class="ftags">
				<input class="button" type="submit" value="Post" />
			</div>
		</form>
	</div>
</body>
</html>
