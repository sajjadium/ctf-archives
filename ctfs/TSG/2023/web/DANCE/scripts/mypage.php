<?php
if (isset($_COOKIE["auth"])) {
    $encrypted_auth = $_COOKIE["auth"];
    $iv = base64_decode($_COOKIE["iv"]);
    $tag = base64_decode($_COOKIE["tag"]);
    $cipher = "aes-128-gcm";
    $key = base64_decode("__REDACTED__");
    $auth = openssl_decrypt($encrypted_auth, $cipher, $key, $options = 0, $iv, $tag);
    $flag = "TSGCTF{__REDACTED__}";
    if ($auth == "admin") {
        $msg = "Hello admin! Password is here.\n" . $flag . "\n";
    } else if ($auth == "guest") {
        $msg = "Hello guest! Only admin can get flag.";
    } else if ($auth == "") {
        $msg = "I know you rewrote cookies!";
    } else {
        $msg = "Hello stranger! Only admin can get flag.";
    }
} else {
    header("Location: index.php");
}
?>
<!DOCTYPE html>
<html>

<head>

</head>

<body>
    <?php echo $msg; ?>
</body>

</html>
