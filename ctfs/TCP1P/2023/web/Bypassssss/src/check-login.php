<?php
	session_start();

	include 'config.php';

	function sanitizeString($input) {
		$pattern = '/[\'"\(\)%=;\.\s-]/';
		$sanitized = preg_replace($pattern, '', $input);
		return $sanitized;
	}

	function removeBadStrings($input) {
		$badStrings = array(
        		'/UNION/i',
        		'/OR/i',
        		'/AND/i',
        		'/BY/i',
        		'/SELECT/i',
        		'/SLEEP/i',
				'/BENCHMARK/i',
        		'/TRUE/i',
        		'/FALSE/i',
				'/\d/'
			);
		$cleanedInput = preg_replace($badStrings, '', $input);
        return $cleanedInput;
	}

	$username = $_POST['username'];
	$password = $_POST['password'];

	$sanitizedUsername = sanitizeString($username);
	$sanitizedPassword = sanitizeString($password);

	$cleanUsername = removeBadStrings($sanitizedUsername);
	$cleanPassword = removeBadStrings($sanitizedPassword);

	$query = "SELECT * FROM admin WHERE username = '$cleanUsername' AND password = '$cleanPassword'";

	$data = mysqli_query($conn, $query);

	$cek = mysqli_num_rows($data);

	if ($cek > 0) {
		$_SESSION["admin_username"] = $sanitizedUsername;
		$_SESSION["admin_status"] = "true";
		header("Location: dashboard.php");
	} else {
		header("Location: index.php?msg=fail");
	}

?>
