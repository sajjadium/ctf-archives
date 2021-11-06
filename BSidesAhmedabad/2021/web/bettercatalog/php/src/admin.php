<?php
include "./include/index.php";
make_header("admin");

if (!isset($_SESSION["user"]) || !$_SESSION["user"]["is_admin"]) {
	flash("error", "<em>ZAP!</em> You must be an admin to view the administration page.");
	send_to_referrer();
}

$stmt = $pdo->prepare("SELECT aq.*, i.title FROM admin_queue aq INNER JOIN issue i ON i.id = aq.issue_id ORDER BY aq.id ASC LIMIT 10");
$success = $stmt->execute();

if (!$success) {
	?>
	<p><em>ZAP!</em> Something went wrong.  Try again in a moment.</p>
	<?php
	exit();
}

$queue = $stmt->fetchAll();
?>
<h1>Pending Issues for Approval</h1>
<?php if(count($queue) == 0) { ?>
	<div class="queue-list">
		<div class="empty">There are no pending approvals.</div>
	</div>
<?php } else { ?>
	<div class="queue-list">
		<?php foreach ($queue as $item) { ?>
			<a class="issue-pending-approval" href="/admin-redirect.php?id=<?php echo $item["id"]; ?>">
				<div class="queue-item">
					<?php echo htmlspecialchars($item["title"]); ?>
				</div>
			</a>
		<?php } ?>
	</div>
<?php } ?>

<?php make_footer(); ?>
