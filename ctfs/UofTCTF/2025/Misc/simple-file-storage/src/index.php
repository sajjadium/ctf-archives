<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple File Storage</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link href="style.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="card p-4 mb-5">
            <h1 class="h3 mb-4 text-center">Simple File Storage</h1>
            <?php if (isset($_SESSION['message'])): ?>
                <div class="alert alert-info alert-dismissible fade show">
                    <?php echo $_SESSION['message']; ?>
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
                <?php unset($_SESSION['message']); ?>
            <?php endif; ?>
            
            <div class="upload-area" id="drop-area">
                <form action="upload.php" method="POST" enctype="multipart/form-data" class="mb-3">
                    <div class="mb-3">
                        <svg class="mb-3" width="50" height="50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                        </svg>
                        <p class="mb-3">Drag and drop your ZIP file here or click to select</p>
                        <input class="form-control" type="file" id="zipFile" name="zipFile" accept=".zip" required>
                    </div>
                    <button type="submit" class="btn btn-primary px-4">Upload</button>
                </form>
            </div>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        $(document).ready(function() {
            const dropArea = $('#drop-area');
            
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropArea.on(eventName, preventDefaults);
            });

            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }

            ['dragenter', 'dragover'].forEach(eventName => {
                dropArea.on(eventName, () => dropArea.addClass('highlight'));
            });

            ['dragleave', 'drop'].forEach(eventName => {
                dropArea.on(eventName, () => dropArea.removeClass('highlight'));
            });

            dropArea.on('drop', handleDrop);

            function handleDrop(e) {
                const dt = e.originalEvent.dataTransfer;
                const files = dt.files;
                $('#zipFile')[0].files = files;
            }
        });
    </script>
</body>
</html>