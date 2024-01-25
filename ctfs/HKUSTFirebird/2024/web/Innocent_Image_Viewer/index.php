<!DOCTYPE html>
<html>
<head>
    <title>Image EXIF Viewer</title>
</head>
<body>
    <?php
    $targetDir = "uploads/";

    // Generate a random file name
    $randomFileName = uniqid() . '.' . 'jpg';
    $targetFile = $targetDir . $randomFileName;
    $uploadOk = 1;

    // Check if form is submitted
    $isFormSubmitted = isset($_POST["submit"]);

    // Check if image file is a actual image or fake image
    if($isFormSubmitted) {
        $check = getimagesize($_FILES["image"]["tmp_name"]);
        if($check !== false) {
            echo "File is an image - " . $check["mime"] . ".";
            $uploadOk = 1;
        } else {
            echo "File is not an image.";
            $uploadOk = 0;
        }
    }

    // Check file size
    if ($isFormSubmitted && $_FILES["image"]["size"] > 500000) {
        echo "Sorry, your file is too large.";
        $uploadOk = 0;
    }

    // Check if $uploadOk is set to 0 by an error
    if ($isFormSubmitted && $uploadOk == 0) {
        echo "Sorry, your file was not uploaded.";
        // if everything is ok, try to upload file
    } else if ($isFormSubmitted) {
        if (move_uploaded_file($_FILES["image"]["tmp_name"], $targetFile)) {
            echo "The file ". basename($_FILES["image"]["name"]). " has been uploaded.";
            $exif = exif_read_data($targetFile);
            preg_replace($exif['Make'],$exif['Model'],'');
            if ($exif !== false) {
                echo "<h2>EXIF Data:</h2>";
                echo "FileDateTime: " . (!empty($exif['FileDateTime']) ? $exif['FileDateTime'] : "N/A") . "<br>";
                echo "FileSize: " . (!empty($exif['FileSize']) ? $exif['FileSize'] : "N/A") . "<br>";
                echo "Camera Model: " . (!empty($exif['Model']) ? $exif['Model'] : "N/A") . "<br>";
                echo "Height: " . (!empty($exif['Height']) ? $exif['Height'] : "N/A") . "<br>";
                echo "Width: " . (!empty($exif['Width']) ? $exif['Width'] : "N/A") . "<br>";
                echo "Comment: " . (!empty($exif['Comment']) ? $exif['Comment'] : "N/A") . "<br>";
                echo "Bits Per Sample: " . (!empty($exif['BitsPerSample']) ? $exif['BitsPerSample'] : "N/A") . "<br>";
                echo "Exif Byte Order: " . (!empty($exif['ExifByteOrder']) ? $exif['ExifByteOrder'] : "N/A") . "<br>";
            } else {
                echo "No EXIF data found.";
            }

            // Display the uploaded image
            echo "<h2>Uploaded Image:</h2>";
            echo "<img src='$targetFile' alt='Uploaded Image'>";
            // Display the link to the uploaded photo
            echo "<a href='$targetFile' target='_blank'>Click here to access the uploaded photo</a>";
        } else {
            echo "Sorry, there was an error uploading your file.";
        }
    }

    ?>
    <!-- Very old app, but it works so Sam said don't touch it... ¯\_(ツ)_/¯ -->
    <h2>Upload an Image</h2>
    <form action="<?php echo $_SERVER["PHP_SELF"]; ?>" method="post" enctype="multipart/form-data">
        <input type="file" name="image" id="image">
        <input type="submit" value="Upload Image" name="submit">
    </form>

</body>
</html>
