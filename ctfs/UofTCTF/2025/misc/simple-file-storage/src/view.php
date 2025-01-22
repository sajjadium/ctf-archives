<?php
session_start();

error_reporting(E_ALL);
ini_set('display_errors', 1);

$extractedDir = __DIR__ . '/extracted/';

$dir = isset($_GET['dir']) ? $_GET['dir'] : '';

if (!preg_match('/^[a-f0-9]+(?:\/[^\/]+)*$/', $dir)) {
    die('Invalid directory parameter');
}

if (strpos($dir, '..') !== false) {
    die('Invalid path');
}

$fullPath = $extractedDir . $dir;
if (!is_dir($fullPath)) {
    die('Directory not found');
}

$files = array_diff(scandir($fullPath), array('.', '..'));

$pathParts = explode('/', $dir);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Uploaded Files</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="style.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="card p-4">
            <nav aria-label="breadcrumb" class="mb-4">
                <ol class="breadcrumb mb-0">
                    <?php
                    $breadcrumbPath = '';
                    foreach ($pathParts as $part):
                        if (empty($part)) continue;
                        $breadcrumbPath .= $part . '/';
                        $trimmedPath = rtrim($breadcrumbPath, '/');
                    ?>
                    <li class="breadcrumb-item">
                        <a href="view.php?dir=<?php echo urlencode($trimmedPath); ?>">
                            <?php echo htmlspecialchars($part); ?>
                        </a>
                    </li>
                    <?php endforeach; ?>
                </ol>
            </nav>

            <h1 class="h3 mb-4">Files and Folders</h1>

            <?php if (empty($files)): ?>
                <div class="text-center p-5">
                    <svg class="mb-3" width="50" height="50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
                    </svg>
                    <p class="text-muted">This folder is empty</p>
                </div>
            <?php else: ?>
                <div class="file-list">
                    <?php foreach ($files as $file):
                        $filePath = $fullPath . '/' . $file;
                        $isDir = is_dir($filePath);
                    ?>
                        <div class="file-item d-flex justify-content-between align-items-center">
                            <?php if ($isDir): ?>
                                <a href="view.php?dir=<?php echo urlencode($dir ? $dir . '/' . $file : $file); ?>" 
                                   class="text-decoration-none text-dark">
                                    <svg class="me-2" width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/>
                                    </svg>
                                    <?php echo htmlspecialchars($file); ?>
                                </a>
                            <?php else: ?>
                                <div class="d-flex justify-content-between align-items-center w-100">
                                    <a href="<?php echo 'extracted/' . $dir . '/' . $file; ?>" 
                                       target="_blank"
                                       class="text-decoration-none text-dark">
                                        <svg class="me-2" width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                                        </svg>
                                        <?php echo htmlspecialchars($file); ?>
                                    </a>
                                    <div>
                                        <a href="<?php echo 'extracted/' . $dir . '/' . $file; ?>" 
                                           target="_blank"
                                           class="btn btn-outline-primary btn-sm me-2">
                                            View
                                        </a>
                                        <a href="download.php?dir=<?php echo urlencode($dir); ?>&file=<?php echo urlencode($file); ?>" 
                                           class="btn btn-primary btn-sm">
                                            Download
                                        </a>
                                    </div>
                                </div>
                            <?php endif; ?>
                        </div>
                    <?php endforeach; ?>
                </div>
            <?php endif; ?>

            <div class="text-center mt-4">
                <a href="index.php" class="btn btn-outline-primary">Upload Another File</a>
            </div>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>