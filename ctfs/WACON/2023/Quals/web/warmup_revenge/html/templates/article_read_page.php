<?php
	if(!defined('__MAIN__')) exit('!^_^!');
	$idx = $_GET['idx'];

	if(!isset($_GET['pass'])) {
		die("No password provided");
	} else {
		$password = md5($_GET['pass']);
		$row = fetch_row('board', array('idx' => $idx, 'password' => $password), 'and');
	}
	if(!$row) die('Not Found');
	if(intval($row['require_level']) > intval($_SESSION['level'])) die('no permisson');

	include(__TEMPLATE__ . 'head.php');

?>
	<style type="text/css">
		.wrap { margin:auto; text-align:center; margin-top: 50px;}
		.box { vertical-align:middle; display:inline-block; }
		.box .in { width:500px; height:30px; background-color:#FFF; text-align: left;}
	</style>

	<div class="wrap">
		<div class="box">
			<div class="in">
				Writer : <b><?=clean_html($row['username'])?></b>
				<hr>
				<?=clean_html($row['title'])?>
				<hr>
				<?=clean_html($row['content'])?>
				<hr>
				<?php
					if($row['file_path']){
						echo '<a id="download" href="/download.php?idx='.$row['idx'].'">Download</a>';
					}
				?>
				<hr>
				<?php 
					if($_SESSION['username'] === $row['username']) echo '<a href="./board.php?p=delete&idx='.$row['idx'].'">Delete</a>';
				?>
				<?php 
					if($_SESSION['username'] === $row['username']) echo '<a href="./report.php?idx='.$row['idx'].'&path='.clean_html($_SERVER['PHP_SELF']).'">Report</a>';
				?>
				<?php
					if($row['file_path']) {
						echo "<script src='./static/javascript/auto.js'></script>";
					}
				?>
			</div>
		</div>
	</div>

<?php
	include(__TEMPLATE__ . 'tail.php');
?>

