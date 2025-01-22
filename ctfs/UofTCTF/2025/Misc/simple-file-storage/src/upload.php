<?php

session_start();

function cleanup($uploadedFile = null, $extractPath = null) {
    if ($uploadedFile && file_exists($uploadedFile)) {
        unlink($uploadedFile);
    }
    
    if ($extractPath && file_exists($extractPath)) {
        exec("rm -rf " . escapeshellarg($extractPath));
    }
}

$uploadDir = __DIR__ . '/uploads/';
$extractedDir = __DIR__ . '/extracted/';
$maxFileSize = 1 * 1024 * 1024; // 1 MB
$forbiddenExtensions = ['php', 'phtml', 'phar', 'ht'];

if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0755, true);
}
if (!is_dir($extractedDir)) {
    mkdir($extractedDir, 0755, true);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_FILES['zipFile'])) {
        $_SESSION['message'] = 'No file uploaded.';
        header('Location: index.php');
        exit();
    }

    $file = $_FILES['zipFile'];

    if ($file['error'] !== UPLOAD_ERR_OK) {
        $_SESSION['message'] = 'File upload error.';
        header('Location: index.php');
        exit();
    }

    if ($file['size'] > $maxFileSize) {
        $_SESSION['message'] = 'File is too large.';
        header('Location: index.php');
        exit();
    }

    if (strpos($file['name'], "\0") !== false) {
        $_SESSION['message'] = 'Invalid file name.';
        header('Location: index.php');
        exit();
    }

    $fileExt = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    if ($fileExt !== 'zip') {
        $_SESSION['message'] = 'Invalid file extension. Only .zip allowed.';
        header('Location: index.php');
        exit();
    }

    $uniqueName = bin2hex(random_bytes(16)) . '.zip';
    $uploadedFilePath = $uploadDir . $uniqueName;
    if (!move_uploaded_file($file['tmp_name'], $uploadedFilePath)) {
        $_SESSION['message'] = 'Failed to move uploaded file.';
        header('Location: index.php');
        exit();
    }

    $f = fopen($uploadedFilePath, 'rb');
    $magicBytes = fread($f, 4);
    fclose($f);
    if ($magicBytes !== "PK\x03\x04") {
        cleanup($uploadedFilePath);
        $_SESSION['message'] = 'Invalid ZIP file magic bytes.';
        header('Location: index.php');
        exit();
    }

    $zip = new ZipArchive;
    if ($zip->open($uploadedFilePath) !== TRUE) {
        cleanup($uploadedFilePath);
        $_SESSION['message'] = 'Failed to open ZIP file.';
        header('Location: index.php');
        exit();
    }

    $files = [];
    for ($i = 0; $i < $zip->numFiles; $i++) {
        $entry = $zip->getNameIndex($i);

        $normalized = str_replace('\\', '/', $entry);

        if (strpos($normalized, '../') !== false || 
            strpos($normalized, '..\\') !== false ||
            strpos($normalized, '/') === 0) {
            $zip->close();
            cleanup($uploadedFilePath);
            $_SESSION['message'] = 'ZIP contains path traversal attempts.';
            header('Location: index.php');
            exit();
        }

        if (strpos($normalized, "\0") !== false) {
            $zip->close();
            cleanup($uploadedFilePath);
            $_SESSION['message'] = 'ZIP contains null bytes in file names.';
            header('Location: index.php');
            exit();
        }

        $zip->getExternalAttributesIndex($i, $opsys, $attr);
        $mode = ($attr >> 16) & 0xFFFF;
        $fileType = $mode & 0xF000;

        if ($fileType === 0xA000) {
            $zip->close();
            cleanup($uploadedFilePath);
            $_SESSION['message'] = 'ZIP contains symlinks.';
            header('Location: index.php');
            exit();
        }

        $baseName = basename($normalized);

        if (strlen($baseName) > 50) {
            $zip->close();
            cleanup($uploadedFilePath);
            $_SESSION['message'] = 'ZIP contains files with names longer than 50 characters.';
            header('Location: index.php');
            exit();
        }

        $ext = strtolower(pathinfo($baseName, PATHINFO_EXTENSION));
        foreach ($forbiddenExtensions as $forbiddenExt) {
            if (strpos($ext, $forbiddenExt) !== false) {
                $zip->close();
                cleanup($uploadedFilePath);
                $_SESSION['message'] = 'ZIP contains forbidden file types.';
                header('Location: index.php');
                exit();
            }
        }

        foreach ($forbiddenExtensions as $forbiddenExt) {
            if (strpos($normalized, '.' . $forbiddenExt) !== false) {
                $zip->close();
                cleanup($uploadedFilePath);
                $_SESSION['message'] = 'ZIP contains forbidden file types.';
                header('Location: index.php');
                exit();
            }
        }

        if (substr($normalized, -1) === '/') {
            continue;
        }

        $files[] = $normalized;
    }
    $zip->close();

    if (empty($files)) {
        cleanup($uploadedFilePath);
        $_SESSION['message'] = 'ZIP file is empty.';
        header('Location: index.php');
        exit();
    }

    $randomDir = bin2hex(random_bytes(8));
    $extractPath = $extractedDir . $randomDir . '/';
    if (!mkdir($extractPath, 0755, true)) {
        cleanup($uploadedFilePath);
        $_SESSION['message'] = 'Failed to create extraction directory.';
        header('Location: index.php');
        exit();
    }
    exec("7z x " . escapeshellarg($uploadedFilePath) . " -o" . escapeshellarg($extractPath) . " -y", $extractOutput, $extractReturn);
    if ($extractReturn !== 0) {
        foreach ($extractOutput as $extractLine) {
        }

        cleanup($uploadedFilePath, $extractPath);
        $_SESSION['message'] = 'Failed to extract ZIP file.';
        header('Location: index.php');
        exit();
    }

    cleanup($uploadedFilePath);

    $viewLink = $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'] . '/view.php?dir=' . $randomDir;

    $_SESSION['message'] = 'File uploaded and extracted successfully. View your files <a href="' . htmlspecialchars($viewLink) . '">here</a>.';
    header('Location: index.php');
    exit();
} else {
    $_SESSION['message'] = 'Invalid request method.';
    header('Location: index.php');
    exit();
}
?>
