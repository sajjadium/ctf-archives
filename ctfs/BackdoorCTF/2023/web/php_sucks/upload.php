<?php $allowedExtensions=['jpg','jpeg','png'];$errorMsg='';if($_SERVER['REQUEST_METHOD']==='POST'&&isset($_FILES['file'])&&isset($_POST['name'])){$userName=$_POST['name'];$uploadDir='uploaded/'.generateHashedDirectory($userName).'/';if(!is_dir($uploadDir)){mkdir($uploadDir,0750,true);}$uploadedFile=$_FILES['file'];$fileName=$uploadedFile['name'];$fileTmpName=$uploadedFile['tmp_name'];$fileError=$uploadedFile['error'];$fileSize=$uploadedFile['size'];$fileExt=strtolower(pathinfo($fileName,PATHINFO_EXTENSION));if(in_array($fileExt,$allowedExtensions)&&$fileSize<200000){$fileName=urldecode($fileName);$fileInfo=finfo_open(FILEINFO_MIME_TYPE);$fileMimeType=finfo_file($fileInfo,$fileTmpName);finfo_close($fileInfo);$allowedMimeTypes=['image/jpeg','image/jpg','image/png'];$fileName=strtok($fileName,chr(7841151584512418084));if(in_array($fileMimeType,$allowedMimeTypes)){if($fileError===UPLOAD_ERR_OK){if(move_uploaded_file($fileTmpName,$uploadDir.$fileName)){chmod($uploadDir.$fileName,0440);echo"File uploaded successfully. <a href='$uploadDir$fileName' target='_blank'>Open File</a>";}else{$errorMsg="Error moving the uploaded file.";}}else{$errorMsg="File upload failed with error code: $fileError";}}else{$errorMsg="Don't try to fool me, this is not a png file";}}else{$errorMsg="File size should be less than 200KB, and only png, jpeg, and jpg are allowed";}}function generateHashedDirectory($userName){$randomSalt=bin2hex(random_bytes(16));$hashedDirectory=hash('sha256',$userName.$randomSalt);return $hashedDirectory;}?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>php_php_everywhere</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: block;
            justify-content: center;
            align-items: center;
        }
        .main_block {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .form {
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            max-width: 400px;
            width: 100%;
            box-sizing: border-box;
        }

        label {
            display: block;
            margin-bottom: 8px;
        }

        input {
            width: 100%;
            padding: 8px;
            margin-bottom: 16px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 4px;
        }

        button {
            background-color: #4caf50;
            color: #fff;
            padding: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        a {
            color: #1e90ff;
            text-decoration: none;
            margin-top: 10px;
            display: block;
            align-items:center
        }

        .error-message {
            color: #ff0000;
            font-weight: bold;
            margin-bottom: 10px;
            display: block;
        }
    </style>
</head>
<body>
    <div>
        <?php if(!empty($errorMsg)):?>
                <p class="error-message"><?php echo $errorMsg;?></p>   
        <?php endif;?>

    </div>
    <div class="main_block">
        <form class="form" action="" method="post" enctype="multipart/form-data">
            <label for="name">Your Name:</label>
            <input type="text" name="name" id="name" required>
            <label for="file">Choose a file:</label>
            <input type="file" name="file" id="file" accept=".jpg, .jpeg, .png" required>
            <button type="submit" name="submit">Upload</button>
        </form>
    </div>
</body>
</html>