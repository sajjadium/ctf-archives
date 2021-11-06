<?php
include "./include/index.php";

if (!isset($_SESSION["user"])) {
	flash("error", "<em>ZAP!</em> You must log in first.");
	send_to_referrer();
}

$stmt = $pdo->prepare("SELECT * FROM issue WHERE author_id = :id");
$success = $stmt->execute([ "id" => $_SESSION["user"]["id"] ]);

if (!$success) {
	flash("error", "<em>ZAP!</em> Something went wrong.");
	send_to_referrer();
}

make_header("self");

$issues = $stmt->fetchAll();

foreach ($issues as $issue) {
?>
	<a href="/issue.php?id=<?php echo $issue["id"]; ?>"><div class="issue"><?php echo htmlspecialchars($issue["title"]); ?></div></a>
<?php
}

make_footer();
?>
