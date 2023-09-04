<?php
    include "db.php";
    header("Cache-Control: no-cache, no-store");
    
    if (!isset($_GET["id"]) || !is_string($_GET["id"])) {
        die("Missing id");
    }

    $stmt = $db->prepare("SELECT * FROM posts WHERE id=?");
    $stmt->execute([$_GET["id"]]);
    $post = $stmt->fetch();

    if (!$post) {
        die("No post was found with that id");
    }
?>
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width" />
        <meta charset="utf-8" />
        <title>leaklessnote</title>
    </head>
    <body>
        <div>
            <h1>leaklessnote</h1>
            <hr />
            <h3><?php echo htmlspecialchars($post["title"]) ?></h3>
            <div id="contents"><?php echo $post["contents"]; ?></div>
            <hr />
            <a href="/">Back</a>
        </div>
    </body>
</html>