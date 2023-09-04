<?php
    include "db.php";
    header("Cache-Control: no-cache, no-store");
    session_start();

    if (!isset($_SESSION["user"])) {
        header("Location: /");
        die();
    }

    if (isset($_GET["query"]) && is_string($_GET["query"])) {
        $stmt = $db->prepare("SELECT * FROM posts WHERE username=? AND contents LIKE ?");
        $stmt->execute([$_SESSION["user"], "%" . $_GET["query"] . "%"]);
        $posts = $stmt->fetchAll();

        if (count($posts) == 0) {
            http_response_code(404);
        }
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
            <?php if (isset($_GET["query"]) && is_string($_GET["query"])) { ?>
                <h4>You searched for <strong><?php echo htmlspecialchars($_GET["query"]) ?></strong>:</h4>
                <ul>
                    <?php
                        foreach ($posts as &$post) {
                            echo "<li><a href='/post.php?id=$post[1]'>" . htmlspecialchars($post["title"]) . "</a></li>";
                        }
                    ?>
                </ul>
                <?php if (count($posts) == 0) { ?>
                    <p>No results found.</p>
                <?php } ?>
            <?php } else { ?>
                <form method="GET">
                    <fieldset>
                        <label for="query">Search</label>
                        <input type="text" placeholder="Search" id="query" name="query">

                        <input class="button-primary" type="submit" value="Search">
                    </fieldset>
                </form>
            <?php } ?>
        </div>
    </body>
</html>