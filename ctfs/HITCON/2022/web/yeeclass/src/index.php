<?php

include("config.php");

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (!isset($_POST["username"]) || $_POST["username"] == "" || !isset($_POST["password"]) || $_POST["password"] == "") {
        die("No username/password");
    }

    if (!preg_match("/^\w{6,12}$/", $_POST["username"])) {
        die("Illegal username!");
    }

    $login_query = $pdo->prepare("SELECT * FROM user WHERE username=?");
    if (!$login_query->execute(array($_POST["username"]))) {
        die("Login Failed.");
    }

    $result = $login_query->fetch(PDO::FETCH_ASSOC);
    
    if (!$result) {
        // auto register
        $register_query = $pdo->prepare("INSERT INTO user (username, password) VALUES (?, ?)");
        $register_query->execute(array($_POST["username"], hash("md5", $_POST["password"])));
        $_SESSION["userid"] = $pdo->lastInsertId();

        $login_query = $pdo->prepare("SELECT * FROM user WHERE id=?");
        $login_query->execute(array($_SESSION["userid"]));

        $result = $login_query->fetch(PDO::FETCH_ASSOC);
    } else {
        if (!hash_equals($result["password"], hash("md5", $_POST["password"]))) {
            die("Invalid password!");
        }
    }

    $_SESSION["userid"] = $result["id"];
    $_SESSION["username"] = $result["username"];
    $_SESSION["userclass"] = $result["class"];
} else if (isset($_GET["logout"])) {
    session_destroy();
    http_response_code(302);
    header("Location: index.php");
    exit;
}

$query = $pdo->query("SELECT * FROM homework");
$homeworks = $query->fetchAll(PDO::FETCH_ASSOC);

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>yeeclass | Home</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div id="main">
        <header id="header">
            <h1>yeeclass</h1>
            <?php include("components/nav.php") ?>
        </header>
        <hr>
        <section id="homework">
            <?php foreach ($homeworks as $row) { ?>
            <article class="homework">
                <h3><?= $row["name"] ?> <?= ($row["open"]) ? '<span class="open">(Open)</span>' : '<span class="closed">(Closed)</span>'; ?></h3>
                <p><?= $row["description"] ?></p>
                <?php if (isset($_SESSION["userid"])) { ?>
                <div class="action">
                    <?php if ($row["public"] || $_SESSION["userclass"] >= PERM_TA) { ?><a href="submission.php?homeworkid=<?= $row['id'] ?>">[Submission List]</a><?php } if (($row["public"] || $_SESSION["userclass"] >= PERM_TA) && $row['open']) { echo '|'; } ?><?php if ($row['open']) { ?><a href="submit.php?homeworkid=<?= $row['id'] ?>">[Submit]</a><?php } ?>
                </div>
                <?php } ?>
            </article>
            <?php } ?>
        </section>
    </div>
</body>
</html>