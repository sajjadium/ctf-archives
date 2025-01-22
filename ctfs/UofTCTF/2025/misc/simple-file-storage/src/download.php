<?php
session_start();

$extractedDir = __DIR__ . '/extracted/';
$dir = isset($_GET['dir']) ? $_GET['dir'] : '';
$file = isset($_GET['file']) ? $_GET['file'] : '';

if (!preg_match('/^[a-f0-9]+(?:\/[^\/]+)*$/', $dir) || strpos($dir, '..') !== false) {
    die('Invalid directory parameter');
}

if (!preg_match('/^[^\/]+$/', $file)) {
    die('Invalid file parameter');
}

$targetPath = realpath($extractedDir . $dir . '/' . $file);

if ($targetPath === false || 
    strpos($targetPath, realpath($extractedDir)) !== 0 || 
    !is_file($targetPath)) {
    http_response_code(404);
    die("File not found");
}
$finfo = finfo_open(FILEINFO_MIME_TYPE);
$mimeType = finfo_file($finfo, $targetPath);
finfo_close($finfo);

header('Content-Description: File Transfer');
header('Content-Type: ' . $mimeType);
header('Content-Disposition: attachment; filename="' . basename($targetPath) . '"');
header('Content-Length: ' . filesize($targetPath));
readfile($targetPath);
exit();
?>
