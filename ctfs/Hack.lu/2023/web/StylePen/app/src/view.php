<?php
// my security guy told me to secure the staff pages 🤷
header("Content-Security-Policy: style-src 'self' 'unsafe-inline'; img-src *; script-src 'self' blob: 'wasm-unsafe-eval'; object-src 'none'; base-uri 'none';");

include_once("include/Cleaner.php");
$cleaner = new Cleaner();

if (is_string($_GET["id"]) && preg_match("/^[0-9a-f]{32}$/", $_GET["id"])) {
    include_once("include/DB.php");
    $submission = get_submission($_GET["id"]);
}

$origin = getenv("ORIGIN") ?: "http://localhost";

?>

<?php include_once("include/html_head.php") ?>

<main class="container">
    <h1>StylePen Spooktober Competition 2023</h1>
    <?php if ($submission) : ?>
        <section>
            <h2><?php if ($submission["winner"]) : ?>🥳 Winning <?php endif ?>Submission by <?= htmlentities($submission["email"]) ?></h2>
            <div class="grid">
                <div>
                    <textarea id="submission-code" class="code-area" readonly><?= htmlentities($submission["css"]) ?></textarea>
                </div>
                <div>
                    <div id="code-output"><?= $cleaner->sanitize($submission["css"]) ?></div>
                </div>
            </div>
        </section>
        <?php if ($_SESSION["loggedin"] && $_SESSION["username"] === "rater") : ?>
            <section>
                <div class="grid">
                    <form method="POST" action="/submit_admin.php">
                        <input type="hidden" name="url" value="<?= htmlentities("$origin/view.php?id={$submission['id']}") ?>">
                        <button type="submit">Recommend contestant's submission</button>
                        <input type="hidden" name="csrf" value="<?= htmlentities($_SESSION["csrf"]) ?>">
                    </form>
                    <div></div>
                </div>
            </section>
        <?php endif ?>
    <?php else : ?>
        <h2>Submission not found</h2>
    <?php endif ?>
</main>
</body>