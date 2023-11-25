<?php
include_once "../includes/session.php";

function cleanup_old_files()
{
    $currentTimestamp = time();
    $uploadsDirectory = "../uploads";
    $files = scandir($uploadsDirectory);
    if(sizeof($files) > 0)
    {
        foreach ($files as $file) 
        {
            if ($file !== '.' && $file !== '..' && $file !== '.htaccess') 
            {
                $filePath = $uploadsDirectory . '/' . $file;
                if (is_file($filePath)) 
                {
                    $fileTimestamp = filemtime($filePath);
                    $timeDifference = $currentTimestamp - $fileTimestamp;
                    // Check if the file is older than 5 minutes (300 seconds)
                    if ($timeDifference > 300)
                        unlink($filePath);
                }
            }
        }
    }
}

try
{
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_SESSION['user']) && $_SESSION['user']['role'] !== "admin") 
    {        
        if(isset($_POST['title']) && isset($_POST['content']))
        {
            cleanup_old_files();

            $target_file = "";
            if(isset($_FILES['image']) && $_FILES['image']['name'] !== "")
            {
                $targetDirectory = '/uploads/';

                $timestamp = microtime(true);
                $timestampStr = str_replace('.', '', sprintf('%0.6f', $timestamp));
                
                $randomFilename = uniqid() . $timestampStr;
                $targetFile = ".." . $targetDirectory . $randomFilename;
                $imageFileType = strtolower(pathinfo($_FILES['image']['name'], PATHINFO_EXTENSION));
                $allowedExtensions = ['jpg', 'jpeg', 'png'];

                $check = false;
                try
                {
                    $check = @getimagesize($_FILES['image']['tmp_name']);
                }
                catch(Exception $exx)
                {
                    throw new Exception("File is not a valid image!");
                }
                if ($check === false) 
                {
                    throw new Exception("File is not a valid image!");
                }
                if (!in_array($imageFileType, $allowedExtensions)) 
                {
                    throw new Exception("Invalid image file type. Allowed types: jpg, jpeg, png");
                }
                if (!move_uploaded_file($_FILES['image']['tmp_name'], $targetFile)) 
                {
                    throw new Exception("Error uploading the image! Try again! If this issue persists, contact a CTF admin!");
                }
                $target_file = $targetDirectory . $randomFilename;
            }

            $title = $_POST['title'];
            $content = $_POST['content'];
            $user_id = $_SESSION['user']['id'];
    
            $sql = $pdo->prepare("INSERT INTO messages (title, content, file, user_id) VALUES (:title, :content, :file, :user_id)");
            $sql->bindParam(':title', $title, PDO::PARAM_STR);
            $sql->bindParam(':content', $content, PDO::PARAM_STR);
            $sql->bindParam(':user_id', $user_id, PDO::PARAM_INT);
            $sql->bindParam(':file', $target_file, PDO::PARAM_STR);
    
            try 
            {
                $sql->execute();
            } 
            catch (PDOException $e) 
            {
                throw new Exception("Could not create request. Please try again! If this issue persists, contact a CTF admin!");
            }
            $_SESSION['success'] = "Message received! An admin will handle your request shortly. You can view your request <a name='message' href='/pages/view_message.php?id=" . $pdo->lastInsertId() ."'>here</a>";
        }
    }
}
catch(Exception $ex)
{
    $_SESSION['error'] = htmlentities($ex->getMessage());
}
header('Location: /pages/contact.php');