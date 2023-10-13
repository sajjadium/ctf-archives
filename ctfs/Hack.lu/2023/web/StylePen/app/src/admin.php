<?php
// my security guy told me to secure the staff pages 🤷
header("Content-Security-Policy: style-src 'self' 'unsafe-inline'; img-src *; script-src 'self' blob: 'wasm-unsafe-eval'; object-src 'none'; base-uri 'none';");

if (!$_SESSION["loggedin"] || $_SESSION["username"] !== "admin") {
    http_response_code(403);
    die("Unauthorized");
}

include_once("include/DB.php");
$winning_submission = get_winning_submission();

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $_SESSION["message"] = "You dummy, we already have a winner! 🍀";
    $_SESSION["message_type"] = "error";
}
?>
<?php include_once("include/html_head.php") ?>

<main class="container">
    <section>
    <h1>Admin Panel - StylePen Spooktober Competition 2023</h1>
    <h2>The current winner is <?= htmlentities($winning_submission["email"]) ?></h2>
    <a href="/view.php?id=<?= htmlentities($winning_submission["id"]) ?>" role="button">View submission</a>
    </section>
    <section>
    <h2>Change winner</h2>
    <form method="POST" action="admin.php">
        <label for="id">New winning submission ID</label>
        <input name="id">
        <input type="hidden" name="csrf" value="<?= htmlentities($_SESSION["csrf"]) ?>">
        <button type="submit">Submit new winner</button>
    </form>
    </section>
</main>
</body>