<?php
$flag = "TSGCTF{__REDACTED__}";
if (isset($_POST["auth"])) {
    if ($_POST["auth"] == "guest") {
        $auth = "guest";
        $cipher = "aes-128-gcm";
        $key = base64_decode("__REDACTED__");
        $ivlen = openssl_cipher_iv_length($cipher);
        $iv = openssl_random_pseudo_bytes($ivlen);
        $encrypted_auth = openssl_encrypt($auth, $cipher, $key, $options = 0, $iv, $tag);
        setcookie("auth", $encrypted_auth, time() + 3600 * 24);
        setcookie("iv", base64_encode($iv), time() + 3600 * 24);
        setcookie("tag", base64_encode($tag), time() + 3600 * 24);
        header("Location: mypage.php");
    } else if (($_POST["auth"] == "admin") and isset($_POST["password"])) {
        if ($_POST["password"] == $flag) {
            $auth = "admin";
            $cipher = "aes-128-gcm";
            $key = base64_decode("__REDACTED__");
            $ivlen = openssl_cipher_iv_length($cipher);
            $iv = openssl_random_pseudo_bytes($ivlen);
            $encrypted_auth = openssl_encrypt($auth, $cipher, $key, $options = 0, $iv, $tag);
            setcookie("auth", base64_encode($encrypted_auth), time() + 3600 * 24);
            setcookie("iv", base64_encode($iv), time() + 3600 * 24);
            setcookie("tag", base64_encode($tag), time() + 3600 * 24);
            header("Location: mypage.php");
        }
    } else {
        header("Location: index.php");
    }
}
?>

<!DOCTYPE html>
<html>

<head>

</head>

<body>
    <form action="index.php" method="POST">
        <input type="submit" name="auth" value="guest" />
    </form>
</body>

</html>
