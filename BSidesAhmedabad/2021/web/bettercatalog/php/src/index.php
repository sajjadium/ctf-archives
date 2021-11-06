<?php include "./include/index.php"; ?>
<?php
$middle_names = ["Quality", "Quotable", "Quixotic", "Quirky", "Quaternary", "Quantile", "Quantum", "Quizical", "Quasi", "Quintessential", "Quantifiable", "Quicksilver", "Quotidien", "Quarantined", "Qwilfish", "Quintuplet", "Quinine", "Quack", "Quiche", "Queueing"];
$middle_name_index = array_rand($middle_names);
$middle_name = $middle_names[$middle_name_index];
?>
<?php make_header("index"); ?>
<h1>Welcome to the Harry <?php echo $middle_name; ?> Bovik Comic Library Catalog</h1>
<p>Looking for comics?  <em>POW!</em>  You're in the right place!</p>
<h2>Featured Issues</h2>
<ul>
	<li><a href="/issue.php?id=1">Action Comics No. 1</a></li>
	<li><a href="/issue.php?id=2">Detective Comics No. 27</a></li>
	<li><a href="/issue.php?id=3">Plaid Comics No. 1</a></li>
</ul>
<?php make_footer(); ?>
