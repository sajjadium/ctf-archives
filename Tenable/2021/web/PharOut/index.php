<?php

include("wrapper.php");

?>

<html>
<head>
	<title>Phar Out!</title>
</head>

<body>

<p>
Upload a file, and I'll hash it with MD5 :-)
</p>
<form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="POST" enctype="multipart/form-data">
<input type="file" name="the_file" />
<input type="hidden" name="s" value="f" />
<input type="submit" name="submit" value="Upload File" />
</form>

<?php

if (isset($_POST['submit']) && $_FILES['the_file']['size'] > 0)
{
	$dest_dir = getcwd() . "/uploads/";

	echo "<br />Submitted<br />";
	$target_file = $dest_dir . basename($_FILES["the_file"]["name"]);
	//print_r($_FILES);
	move_uploaded_file($_FILES["the_file"]["tmp_name"], $target_file);

	if ($_POST['s'] === 'p')
		$s = 'phar://';
	else
		$s = 'file://';
	echo md5_file("$s$target_file");
	unlink($target_file);
}

?>

</body>

</html>
