<?php
    session_start();

    if ($_SESSION["admin_status"] != "true") {
        header("Location: index.php?msg=login_first");
    }

    function sanitizeImagePath($imagePath) {
        $blacklist = array("./", "\\");

        $sanitizedPath = str_replace($blacklist, "", $imagePath);

        if (strpos($sanitizedPath, "images/") !== 0) {
            $sanitizedPath = "assets/img/" . $sanitizedPath;
        } else {
            echo "Invalid path";
        }

        return $sanitizedPath;
    }

    function displayImage($imagePath) {
        header("Content-Type: image/jpeg");
        readfile($imagePath);
    }

    if (isset($_GET['image'])) {
        $imagePath = $_GET['image'];
        $sanitizedImagePath = sanitizeImagePath($imagePath);
        displayImage($sanitizedImagePath);
    } else {
        echo "Image parameter not provided.";
    }
?>
