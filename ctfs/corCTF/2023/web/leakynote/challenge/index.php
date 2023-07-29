<?php
    include "db.php";
    session_start();

    if (isset($_SESSION["user"]) && $_SERVER['REQUEST_METHOD'] === 'POST') {
        if ($_SESSION["user"] === "admin") {
            die("Sorry, no changing the admin account!");
        }

        if (isset($_POST["title"]) && is_string($_POST["title"]) && isset($_POST["contents"]) && is_string($_POST["contents"])) {
            $title = substr($_POST["title"], 0, 32);
            $contents = substr($_POST["contents"], 0, 100);
            $stmt = $db->prepare("INSERT INTO posts (username, id, title, contents) VALUES (?, ?, ?, ?)");
            $stmt->execute([$_SESSION["user"], bin2hex(random_bytes(8)), $title, $contents]);
        }
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
            <?php if (!isset($_SESSION["user"])) { ?>
                <a class="button" href="/login.php">Login</a>
                <a class="button" href="/register.php">Register</a>
            <?php } else { ?>
                <h4>Your posts:</h4>
                <ul>
                    <?php
                        $stmt = $db->prepare("SELECT * FROM posts WHERE username=?");
                        $stmt->execute([$_SESSION["user"]]);
                        $posts = $stmt->fetchAll();

                        foreach ($posts as &$post) {
                            echo "<li><a href='/post.php?id=$post[1]'>" . htmlspecialchars($post["title"]) . "</a></li>";
                        }
                    ?>
                </ul>
                <h5><a href="/search.php">Search for a post</a></h5>
                <h4>Create a new post:</h4>
                <form method="POST">
                <fieldset>
                    <label for="title">Title</label>
                    <input type="text" placeholder="Title" id="title" name="title">

                    <label for="contents">Contents</label>
                    <textarea id="contents" name="contents"></textarea>

                    <input class="button-primary" type="submit" value="Create">
                </fieldset>
            </form>
            <?php } ?>
        </div>
    </body>
</html>