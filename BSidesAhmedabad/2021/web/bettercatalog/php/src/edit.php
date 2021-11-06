<?php
include "./include/index.php";

if (!isset($_SESSION["user"])) {
	header("Location: /");
	exit();
}

make_header("edit");

if (isset($_GET["id"]) && !is_numeric($_GET["id"])) {
	http_response_code(400);
	exit();
}

if (isset($_GET["id"])) {
	$stmt = $pdo->prepare("SELECT * FROM issue WHERE id = :id");
	$success = $stmt->execute([ "id" => $_GET["id"] ]);

	if (!$success) {
		die_404();
	}

	$issue = $stmt->fetch();

	if (!$issue) {
		die_404();
	}

	if ($issue["draft"] && (!isset($_SESSION["user"]) || $issue["author_id"] != $_SESSION["user"]["id"])) {
		die_404();
	}
} else {
	$issue = [ "image" => "", "title" => "", "content" => "" ];
}
?>
<form class="edit" action="/post.php" method="POST">
	<input type="hidden" name="id" value="<?php if (isset($_GET["id"])) { echo $_GET["id"]; } ?>" />
	<input class="title" type="text" name="title" placeholder="Title" value="<?php echo htmlspecialchars($issue["title"]); ?>" />
	<input class="image-url" type="text" name="image" placeholder="Image URL" value="<?php echo htmlspecialchars($issue["image"]); ?>" />
	<textarea name="content" rows="20" placeholder="Content (use two newlines for paragraph break, square brackets for emphasis)"><?php echo htmlspecialchars($issue["content"]); ?></textarea>
	<button>Submit</button>
</form>

<?php make_footer(); ?>
