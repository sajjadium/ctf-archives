<?php $encrypted_text=base64_decode('Xg0aAhhab18LChIcWmgMCE89RA0CHwBWEwELCQsLVAkcQwUKGQ5IaFkMHUpuMQsMRRAJBQVfTj0nHyNTGwJFUjsWDV0wBwxVFFw6RgM7DlUYXAluWQEbW3xZSwAKChZKbllMAREbCVo=');
$password = isset($_REQUEST['password']) ? $_REQUEST['password'] : "-";
$decrypted_text = '';

for($i = 0; $i < strlen($encrypted_text); $i++){
	$currentpasswordChar = ord($password[$i % strlen($password)]);
	$decrypted_text.=chr(($currentpasswordChar^ord($encrypted_text[$i]))%256);
}


if(MD5($decrypted_text)=='a8379015e5a77cfe783b87b3058672f3'){
	echo $decrypted_text;
}else {
	echo '<form method="post" action="EtTuBrute.php"><input type="text" name="password" value=""/><input type="submit" value="&gt;"/></form>';
}
?>