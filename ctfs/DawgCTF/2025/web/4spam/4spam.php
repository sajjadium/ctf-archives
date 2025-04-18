<?php

session_start([
    'cookie_httponly' => true,
    'use_strict_mode' => true,
]);

if (!isset($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

$uploadsDir = __DIR__ . '/uploads';
$maxSize    = 5 * 1024 * 1024; // 5 MB
$allowedExt = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'webp'];

function getDb(): PDO
{
    static $db = null;

    if ($db === null) {
        $db = new PDO(
            'sqlite:/tmp/imageboard.db'
        );

        $db->exec("CREATE TABLE IF NOT EXISTS posts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            message     TEXT NOT NULL,
            image       TEXT,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )");
    }

    return $db;
}

try {
    $db = getDb();
} catch (PDOException $e) {
    die('Database error: ' . $e->getMessage());
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $csrf = $_POST['csrf_token'] ?? '';
    if (!hash_equals($_SESSION['csrf_token'], $csrf)) {
        die('Invalid CSRF token.');
    }

    $message  = trim($_POST['message']  ?? '');
    $imageRel = null;

    if ($message === '') {
        header('Location: ' . htmlspecialchars(basename(__FILE__)));
        exit;
    }

    if (!empty($_FILES['image']['name'])) {
        $ext = strtolower(pathinfo($_FILES['image']['name'], PATHINFO_EXTENSION));

        if (!in_array($ext, $allowedExt, true)) {
            die('Unsupported file type.');
        }
        if ($_FILES['image']['size'] > $maxSize) {
            die('File exceeds maximum size of 5 MB.');
        }
        if (!is_dir($uploadsDir) && !mkdir($uploadsDir, 0755, true)) {
            die('Failed to create uploads directory.');
        }

        $filename = uniqid('img_', true) . '.' . $ext;
        $dest     = $uploadsDir . '/' . $filename;

        if (!move_uploaded_file($_FILES['image']['tmp_name'], $dest)) {
            die('Failed to move uploaded file.');
        }
        $imageRel = 'uploads/' . $filename;

        if ($ext == 'pdf') {
            exec("gs -dBATCH -dNOSAFER -dNODISPLAY -dNOPAUSE -sDEVICE=jpeg -dLastPage=1 -r100 -sOutputFile={$imageRel}_proc.jpg $imageRel");
            exec("convert {$imageRel}_proc.jpg -thumbnail 100x100^ -gravity center -extent 100x100 {$imageRel}_thumb.jpg");
        } else {
            exec("convert $imageRel -thumbnail 100x100^ -gravity center -extent 100x100 {$imageRel}_thumb.jpg");
        }
    }

    $stmt = $db->prepare('INSERT INTO posts (message, image) VALUES (?,?)');
    $stmt->execute([$message, $imageRel]);

    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));

    header('Location: ' . htmlspecialchars(basename(__FILE__)));
    exit;
}

$posts = $db->query('SELECT * FROM posts ORDER BY id DESC')->fetchAll(PDO::FETCH_ASSOC);

?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>4spam</title>
<style>
    :root {
        font-family: arial, helvetica, sans-serif;
        font-size: 13.333px;
        background: #EEF2FF;
    }
    .container { max-width: 1000px; margin: auto; padding: 1rem; }
    h1        { font-family: Tahoma, sans-serif; font-weight: 700; text-align: center; margin-bottom: 1rem; color: rgb(175, 10, 15); }
    form      { background: #fff; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,.07); padding: 1rem; margin-bottom: 2rem; }
    .post     { margin-bottom: 2rem; }
    textarea, input[type="text"] { width: 100%; padding: .5rem; margin-top: .25rem; box-sizing: border-box; }
    label     { display: block; margin-top: .5rem; font-weight: 600; }
    button    { margin-top: .75rem; padding: .5rem 1.25rem; border: none; border-radius: 4px; cursor: pointer; }
    .meta     { color: #444; margin-bottom: .5rem; }
    .post img { max-width: 100px; height: auto; margin-top: .5rem; float: left; margin-right: 1rem; margin-bottom: 2rem;}
    .gt       { color: rgb(120, 153, 34); }
</style>
</head>
<body>
<div class="container">
    <h1>/dawg/ - DawgCTF</h1>

    <form action="" method="post" enctype="multipart/form-data">
        <input type="hidden" name="csrf_token" value="<?= htmlspecialchars($_SESSION['csrf_token']) ?>">

        <label>Message
            <textarea name="message" rows="3" required></textarea>
        </label>

        <label>Image (optional, max 5 MB)
            <input type="file" name="image" accept="image/*">
        </label>

        <button type="submit">Post</button> &nbsp; <abbr title="We can see all your IP addresses and so can the CTF platform. C'mon be nice don't make us clean it up <3&#10;&#13;Also it'll get wiped/restarted every 10 minutes or so probably">Sus?</abbr>
    </form>

    <?php foreach ($posts as $post): ?>
        <hr style="border-bottom-color:rgb(0, 0, 0);border-bottom-style:none;border-bottom-width:0px;border-image-outset:0;border-image-repeat:stretch;
                   border-image-slice:100%;border-image-source:none;border-image-width:1;border-left-color:rgb(0, 0, 0);border-left-style:none;border-left-width:0px;border-right-color:rgb(0, 0, 0);border-right-style:none;border-right-width:0px;
                   border-top-color:rgb(183, 197, 217);border-top-style:solid;border-top-width:1px;clear:both;display:block;height:0px;margin-block-end:6.66667px;margin-block-start:6.66667px;margin-inline-end:0px;margin-inline-start:0px;">
        <div class="post">
            <?php if ($post['image']): ?>
                <a href="<?= htmlspecialchars($post['image']) ?>" target="_blank"><img src="<?= htmlspecialchars($post['image']) ?>_thumb.jpg" alt="uploaded image"></a>
            <?php endif; ?>
            <div class="meta">
                <strong style="color: rgb(17, 119, 67)">Anonymous</strong>
                <?= htmlspecialchars(date('d/m/y(D)H:i:s', strtotime($post['created_at']))) ?>
            </div>
            <p>
                <?php
                $lines = explode("\n", $post['message']);
                foreach ($lines as $line) {
                    if (str_starts_with($line, '>')) {
                        echo '<span class="gt">' . htmlspecialchars($line) . "</span><br>\n";
                    } else {
                        echo htmlspecialchars($line) . "<br>\n";
                    }
                }
                ?>
            </p>
        </div>
    <?php endforeach; ?>
</div>
</body>
</html>
