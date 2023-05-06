<?php

include("config.php");
include("turnstile.php");

// handle new submission / submission deletion
if ($_SERVER["REQUEST_METHOD"] == "POST" || isset($_GET["delete"])) {
    if (!isset($_SESSION["userid"])) {
        http_response_code(403);
        die("Please login!");
    }

    $homeworkid = (isset($_GET["delete"])) ? $_GET["homeworkid"] : $_POST["homeworkid"];
    
    if (!isset($homeworkid)) {
        http_response_code(400);
        die("Please specify homework id");
    }
    
    $homework_query = $pdo->prepare("SELECT id, `open` FROM homework WHERE id=?");
    $homework_query->execute(array($homeworkid));
    $result = $homework_query->fetch();

    if (!$result) {
        http_response_code(404);
        die("Homework not found");
    }

    if (!$result["open"]) {
        http_response_code(400);
        die("Homework has been closed, no more changes!");
    }
    
    $submission_query = $pdo->prepare("SELECT * FROM submission WHERE userid=? AND homeworkid=?");
    $submission_query->execute(array($_SESSION["userid"], $homeworkid));
    $result = $submission_query->fetch();

    if (!$result) {
        if (isset($_GET["delete"])) {
            // deletion
            http_response_code(404);
            die("No submission to delete");
        } else {
            // new submission
            if (strlen($_POST["content"]) > 100) {
                http_response_code(400);
                die("Content too long");
            }

            $turnstile_response = $_POST["cf-turnstile-response"];
            if (!verify_turnstile($turnstile_response)) {
                http_response_code(403);
                die("Bot verification failed.");
            }

            $id = uniqid($_SESSION["username"]."_");
            $submit_query = $pdo->prepare("INSERT INTO submission (`hash`, userid, homeworkid, content) VALUES (?, ?, ?, ?)");
            $submit_query->execute(array(
                hash("sha1", $id),
                $_SESSION["userid"],
                $_POST["homeworkid"],
                $_POST["content"]
            ));

            $hash_query = $pdo->prepare("SELECT `hash` FROM submission WHERE userid=? AND homeworkid=?");
            $hash_query->execute(array($_SESSION["userid"], $_POST["homeworkid"]));
            $result = $hash_query->fetch();

            http_response_code(302);
            header("Location: submission.php?hash={$result['hash']}");
            exit;
        }
    } else {
        if (!isset($_GET["delete"])) {
            // there is a submission already
            http_response_code(409);
            die("Please delete old submission first!");
        } else {
            if (!hash_equals($_GET["delete"], $result["hash"])) {
                http_response_code(403);
                die("No permission to delete");
            }

            $delete_query = $pdo->prepare("DELETE FROM submission WHERE `hash`=?");
            if ($delete_query->execute(array($result["hash"]))) {
                echo "Deleted";
            } else {
                echo "Error occurs while deleting submission.";
            }
            exit;
        }
    }

    // should not reach
    exit;
} else {
    $submission_query = $pdo->prepare("SELECT `hash` FROM submission WHERE userid=? AND homeworkid=?");
    $submission_query->execute(array($_SESSION["userid"], $_GET["homeworkid"]));
    $result = $submission_query->fetch();

    // redirect to submission
    if ($result) {
        http_response_code(302);
        header("Location: submission.php?hash={$result['hash']}");
        exit;
    }
}

// render submit form
$query = $pdo->query("SELECT id, `name` FROM homework WHERE open=1");
$homeworks = $query->fetchAll(PDO::FETCH_ASSOC);

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>yeeclass | Submit</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div id="main">
        <header id="header">
            <h1>yeeclass</h1>
            <?php include("components/nav.php") ?>
        </header>
        <hr>
        <section id="submit">
            <form action="submit.php" method="POST">
                <div class="row">
                    <label for="homework">Choose Homework:</label>
                    <select id="homeworkid" name="homeworkid">
                        <?php foreach ($homeworks as $row) { ?>
                        <option value="<?= $row['id'] ?>"<?php if ($row["id"] == $_GET["homeworkid"]) { ?>selected="selected"<?php } ?>><?= $row["name"] ?></option>
                        <?php } ?>
                    </select>
                </div>
                <div class="row">
                    <label for="content">Input Content: (atmost 100 characters)</label>
                    <br>
                    <textarea id="content" name="content" cols="5" maxlength="100"></textarea>
                </div>
                <?php if (isset($turnstile_sitekey)) { ?>
                <div class="cf-turnstile" data-sitekey="<?= $turnstile_sitekey ?>"></div> 
                <?php } ?>
                <input type="submit" value="Submit">
            </form>
        </section>
    </div>
    <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
</body>
</html>