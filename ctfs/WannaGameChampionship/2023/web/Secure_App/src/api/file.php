<?php

session_start();

if (!@$_SESSION["isLoggedIn"]) {
	header("Location: /index.php");
	die();
}

if ($_SESSION["username"] !== "admin") {
	http_response_code(403);
	die(file_get_contents("403.html"));
}

function isValidSvg($content)
{

    $tempFile = tempnam(sys_get_temp_dir(), 'svg_');
    file_put_contents($tempFile, $content);

    $mimeType = mime_content_type($tempFile);


    if ($mimeType === 'image/svg+xml') {
        return true;
    }

    unlink($tempFile);

    return false;
}

if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $json = file_get_contents('php://input');

    $data = json_decode($json, true);

    if (isset($data["filename"]) && isset($data["base64_content"]) && is_string($data["base64_content"]) && is_string($data["filename"])) {
        $ext = pathinfo($data["filename"], PATHINFO_EXTENSION);
        if (preg_match("/svg|png|gif|^j/", $ext)) {
            $content = base64_decode($data["base64_content"]);
            if (imagecreatefromstring($content)) {
                $new_name = uniqid() . ".$ext";
                file_put_contents($new_name, $content);
                if ($_SERVER['HTTP_REFERER'] !== 'http://' . $_SERVER['HTTP_HOST'] . '/admin.php') {
                    header("Location: /api/$new_name");
                    die();
                } else die("/api/$new_name");
            } else if (isValidSvg($content)) {
                $new_name = uniqid() . ".$ext";
                file_put_contents($new_name, $content);
                if ( $_SERVER['HTTP_REFERER'] !== 'http://' . $_SERVER['HTTP_HOST'] . '/admin.php') {
                    header("Location: /api/$new_name");
                    die();
                } else die("/api/$new_name");
            } else die("Only support .svg, .png, .jpg, .jpeg, .gif");
        } else {
            die("Not support file upload format");
        }
    } else {
        die("Invalid json body");
    }
}
