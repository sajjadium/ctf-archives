<?php

if (isset($_GET['source'])) {
    highlight_file(__FILE__);
    die();
}

$isEvil = fn($input) => str_starts_with($input, '/') || str_contains($input, "..") || str_contains($input, 'php');
$hacking = fn() => die('Hacking attempt');

$fileLimit = 10000; // File explorer for ants

$username = $_SERVER['HTTP_REMOTE_USER'];
$datadir = sys_get_temp_dir() . '/data';

if ($isEvil($username)) {
    $hacking();
}

$userdir = "$datadir/$username";

if (!file_exists($userdir)) {
    mkdir($userdir, 0777, true);
    file_put_contents("$userdir/hello", "world");
}

chdir($userdir);

if (!empty($_FILES['upload']) && !empty($_POST['target'])) {
    error_log("[uploading file request] user: $username, upload_name: {$_FILES['upload']['name']}, name: {$_POST['target']}");

    if ($isEvil($_POST['target']) || $_FILES['upload']['size'] > $fileLimit) $hacking();

    error_log("[uploading file] user: $username, upload_name: {$_FILES['upload']['name']}, name: {$_POST['target']}");

    file_put_contents($_POST['target'], file_get_contents($_FILES['upload']['tmp_name'], $_POST['target']));
}

if (!empty($_GET['file'])) {
    $file = "$userdir/{$_GET['file']}";
    $mime = mime_content_type($file);

    header("content-type: $mime");

    die(file_get_contents("$userdir/{$_GET['file']}"));
}

$files = scandir($userdir);

?>
<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Awesome filemanager</title>
    <meta name="description" content="Just a pure semantic HTML markup, without .classes.  Built with Pico CSS.">

    <!-- Pico.css (Classless version) -->
    <link rel="stylesheet" href="https://unpkg.com/@picocss/pico@latest/css/pico.classless.min.css">
</head>

<body>

<main>
    <section>
        <h1>File manager</h1>
        List, view and upload your personnel files. <a href="/?source">Source code</a>.<br>
        <br>
        You can upload files from your local computer.
    </section>

    <section>
        <ul>
            <?php foreach ($files as $file) { ?>
                <?php if (!is_file("$userdir/$file")) continue ?>

                <li><a href="/?file=<?php echo $file; ?>"><?php echo $file; ?></a></li>
            <?php } ?>
        </ul>
    </section>

    <section>
        <form method="post" enctype="multipart/form-data">
            <input name="target" type="text" value="example.txt">
            <input name="upload" type="file" id="upload">
            <input type="submit" value="Upload">
        </form>
    </section>
</main>
