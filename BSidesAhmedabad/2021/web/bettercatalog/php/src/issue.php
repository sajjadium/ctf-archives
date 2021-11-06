<?php
include "./include/index.php";
make_header("issue");

if (!is_numeric($_GET["id"])) {
	die_404();
}

$stmt = $pdo->prepare("SELECT * FROM issue WHERE id = :id");
$success = $stmt->execute([ "id" => $_GET["id"] ]);

if (!$success) {
	die_404();
}

$issue = $stmt->fetch();

if (!$issue) {
	die_404();
}

$can_read =
	!$issue["draft"]
	|| (
		isset($_SESSION["user"])
		&& (
			$issue["author_id"] == $_SESSION["user"]["id"]
			|| $_SESSION["user"]["is_admin"]
		)
	);
?>
<?php if($can_read) { ?>
	<div class="image">
		<img src="<?php echo $issue["image"]; ?>" />
	</div>
<?php } ?>
<h1>
	<?php echo htmlspecialchars($issue["title"]); ?>
	<?php if (isset($_SESSION["user"]) && $_SESSION["user"]["id"] == $issue["author_id"]) { ?>
		<div class="edit">Edit this Issue</div>
		<button class="report">Submit for Admin Approval</button>
		<form id="report-form" class="hidden" action="report.php" method="POST">
			<input type="hidden" name="id" value="<?php echo $_GET["id"]; ?>" />
			<input type="hidden" name="token" value="" />
		</form>
	<?php } ?>
</h1>
<?php if (!$can_read) { ?>
	<div class="content">
		<p>This issue does not yet have a public description.</p>
	</div>
<?php } else { ?>
	<div class="content">
		<?php
		function add_emphasis($str) {
			return preg_replace("/\\[(.+?)\\]/s", "<em>$1</em>", $str);
		}

		$base_content = htmlspecialchars($issue["content"]);
		$paragraphs = preg_split("\r?\n\r?\n", $base_content);
		$paragraphs = array_map("add_emphasis", $paragraphs);
		$content = "<p>" . implode("</p><p>", $paragraphs) . "</p>";
		echo $content;
		?>
	</div>
<?php } ?>

<?php make_footer(); ?>
