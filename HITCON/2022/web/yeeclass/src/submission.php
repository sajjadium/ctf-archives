<?php

include("config.php");

if (isset($_GET["hash"]) && $_GET["hash"] != "") {
    // view single submission
    $mode = "view";
    $submission_query = $pdo->prepare("SELECT s.*, u.username, h.name from submission s LEFT JOIN user u ON u.id=s.userid LEFT JOIN homework h ON h.id=s.homeworkid WHERE s.`hash`=?");
    $submission_query->execute(array($_GET["hash"]));
    $result = $submission_query->fetch(PDO::FETCH_ASSOC);

    if (!$result) {
        http_response_code(404);
        die("Submission not found.");
    }
} else {
    // list submissions
    if (isset($_GET["homeworkid"])) {
        $homework_query = $pdo->prepare("SELECT * FROM homework WHERE id=?");
        $homework_query->execute(array($_GET["homeworkid"]));
        $result = $homework_query->fetch(PDO::FETCH_ASSOC);

        if (!$result) {
            http_response_code(404);
            die("Homework not found");
        }

        if ($_SESSION["userclass"] < PERM_TA && !$result["public"]) {
            http_response_code(403);
            die("No permission");
        }

        $mode = "homeworklist";
        $total_query = $pdo->prepare("SELECT COUNT(*) FROM submission WHERE homeworkid=?");
        $total_query->execute(array($_GET["homeworkid"]));
        $total = $total_query->fetchColumn(0);

        $page = max(1, min(intval($_GET["page"]), ceil($total / 10)));
        
        $list_query = $pdo->prepare("SELECT s.*, u.username, h.name, h.public FROM submission s LEFT JOIN user u ON u.id=s.userid LEFT JOIN homework h ON h.id=s.homeworkid WHERE s.homeworkid=? ORDER BY s.time DESC LIMIT 10 OFFSET ?");
        $list_query->bindValue(1, $_GET["homeworkid"]);
        $list_query->bindValue(2, ($page - 1) * 10, PDO::PARAM_INT);
        $list_query->execute();
        $result = $list_query->fetchAll(PDO::FETCH_ASSOC);
    } else if (isset($_SESSION["userid"])) {
        $mode = "userlist";
        $total_query = $pdo->prepare("SELECT COUNT(*) FROM submission WHERE userid=?");
        $total_query->execute(array($_SESSION["userid"]));
        $total = $total_query->fetchColumn(0);
        
        $page = max(1, min(intval($_GET["page"]), ceil($total / 10)));
        
        $list_query = $pdo->prepare("SELECT s.*, u.username, h.name, h.public FROM submission s LEFT JOIN user u ON u.id=s.userid LEFT JOIN homework h ON h.id=s.homeworkid WHERE s.userid=? ORDER BY s.time DESC LIMIT 10 OFFSET ?");
        $list_query->bindValue(1, $_SESSION["userid"]);
        $list_query->bindValue(2, ($page - 1) * 10, PDO::PARAM_INT);
        $list_query->execute();
        $result = $list_query->fetchAll(PDO::FETCH_ASSOC);
    } else {
        http_response_code(400);
        die("Insufficient parameters");
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>yeeclass | Submission</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div id="main">
        <header id="header">
            <h1>yeeclass</h1>
            <?php include("components/nav.php"); ?>
        </header>
        <hr>
        <?php if ($mode == "view") { ?>
        <section id="view">
            <h3><?= $result["username"] ?>_<?= $result["name"] ?> <a href="submit.php?homeworkid=<?= $result['homeworkid'] ?>&delete=<?=  $result['hash'] ?>">[Delete]</a></h3>
            <p>Time: <?= $result["time"] ?></p>
            <p>Score: <?= $result["score"] ?? "(Not judged)" ?></p>
            <pre><?= htmlspecialchars($result["content"]) ?></pre>
        </section>
        <?php } else { ?>
        <section id="list">
            <table>
                <thead>
                    <tr>
                        <th>Homework</th>
                        <th>Score</th>
                        <th>Submitted By</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($result as $row) { ?>
                    <tr>
                        <?php if ((isset($_SESSION["userid"]) && $_SESSION["userclass"] >= PERM_TA) || $row["userid"] == $_SESSION["userid"]) { ?>
                        <td><a href="submission.php?hash=<?= $row['hash'] ?>"><?= $row["name"] ?></a></td>
                        <?php } else { ?>
                        <td><?= $row["name"] ?></td>
                        <?php } ?>
                        <td><?= $row["score"] ?? "-" ?></td>
                        <td><?= $row["username"] ?></td>
                        <td><?= $row["time"] ?></td>
                    </tr>
                    <?php } ?>
                </tbody>
            </table>
            <p class="total">Total: <?= $total ?> submission(s).</p>
            <p class="pager">
                <?php if ($page > 1) { ?><a href="submission.php?<?php if ($mode == "homeworklist") { ?>homeworkid=<?= $_GET['homeworkid'] ?>&<?php } ?>page=<?= $page - 1;?>">[&lt;- Prev Page]</a><?php } ?>
                <?php if ($page * 10 < $total) { ?><a href="submission.php?<?php if ($mode == "homeworklist") { ?>homeworkid=<?= $_GET['homeworkid'] ?>&<?php } ?>page=<?= $page + 1;?>">[Next Page -&gt;]</a><?php } ?>
            </p>
        </section>
        <?php } ?>
    </div>
</body>
</html>