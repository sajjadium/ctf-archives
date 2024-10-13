<?php
function makeimg($data, $imgPath, $mime) {
    $img = imagecreatefromstring($data);
    switch($mime){
        case 'image/png':
            $with_ext = $imgPath . '.png';
            imagepng($img, $with_ext);
            break;
        case 'image/jpeg':
            $with_ext = $imgPath . '.jpg';
            imagejpeg($img, $with_ext);
            break;
        case 'image/webp':
            $with_ext = $imgPath . '.webp';
            imagewebp($img, $with_ext);
            break;
        case 'image/gif':
            $with_ext = $imgPath . '.gif';
            imagegif($img, $with_ext);
            break;
        default:
            $with_ext = 0;
            break;
        }
    return $with_ext;
}

if(isset($_POST["url"])){ 
    $cdn_url = 'http://localhost:8080/cdn/' . $_POST["url"];
    $img = @file_get_contents($cdn_url);
    $f = finfo_open();
    $mime_type = finfo_buffer($f, $img, FILEINFO_MIME_TYPE);
    $fileName = 'uploads/' . substr(md5(rand()), 0, 13);
    $success = makeimg($img, $fileName, $mime_type);
    if ($success !== 0) {
        $msg = $success;
    }
} 
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        body {
            background-color: black;
            text-align: center;
        }
        .center {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        label, p, h1, h3 {
            color: white;
        }
        form {
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="center">
            <h1> MAKIMA IS LISTENING</h1>
            <img width="1200" height="1200" src="uploads/makima.png">
            <h3> Submit Makima fan art: </h3>
            <?php if (isset($msg)) { ?>
                <p>Message: <?= htmlspecialchars($msg) ?></p>
            <?php } ?>
            <form method="post">
            <label>Upload Image:</label>
            <input type="text" name="url">
            </form>
    </div>
</body>

</html>
