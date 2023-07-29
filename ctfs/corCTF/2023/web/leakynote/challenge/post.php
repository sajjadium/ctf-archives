<?php
    include "db.php";
    
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
        <title>leakynote</title>
        <link rel="stylesheet" href="/assets/normalize.css" />
        <link rel="stylesheet" href="/assets/milligram.css" />
    </head>
    <body>
        <br />
        <div class="container">
            <h1>leakynote</h1>
            <hr />
            <h3><?php echo htmlspecialchars($post["title"]) ?></h3>
            <div id="contents"><?php echo $post["contents"]; ?></div>
            <hr />
            <a href="/">Back</a>
        </div>
    </body>
</html>