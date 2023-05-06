<?php
session_start();
?>
<!DOCTYPE>
<html>
<head>
	<script src='../js/main.js'></script>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Blog</title>
        <link rel="stylesheet" type="text/css" href="../css/styles.css" />
</head>
<body>
	<div class="nav-top">
		<ul class="points">
			<li style="border-right: 1px solid white;"><a href="../index.php">Blog</a></li>
			<li style="background-color: #ff2600;"><a href="posts.php">Posts</a></li>
		</ul>
	</div>
	<div class="container">
<?php
require("../class.php");
require("../db/config.php");
if (!isset($_SESSION["username"])) {
if (!empty($_GET['token'])){
		 try {	
	     $result= unserialize(base64_decode($_GET['token']))->get_post();
	 }catch (Error $e) {
	 	 echo unserialize(base64_decode($_GET['token']));

	 }

	}
}
else{
if (!empty($_GET['token'])){	
	     try {	
	     unserialize(base64_decode($_GET['token']))->get_post();
	 }catch (Error $e) {
	 	 echo unserialize(base64_decode($_GET['token']));

	 }
	}
else{
if (!($res = $conn->prepare("SELECT name, content FROM Blog_posts1 WHERE poster=?")))
	die('Can\'t get your blogs :-(');
if (!($res->bind_param("s", $_SESSION["username"])) || !($res->execute()) || !($result = $res->get_result()))
	die('Can\'t get your blogs :-(');
if ($result->num_rows > 0) {
	while ($row = $result->fetch_assoc()) {
		echo $row["content"].'<br>';
	}
}
else {
	echo '<p class="error">You don\'t have any blogs yet.</p>';
}
}
}
?>
	</div>
</body>
</html>
