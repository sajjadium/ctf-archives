<?php
	if(!defined('__MAIN__')) exit('!^_^!');
	
	$idx = trim($_GET['idx']);
	$query = array(
		'idx' => $idx,
		'to_id' => $_SESSION['username']
	); 
	$row = fetch_row('note', $query, 'and');
	if(!$row) die('Not Found');

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
				<b>From : </b>   <?=clean_html($row['from_id']) ?>
				<hr>
				<?=clean_html($row['date']) ?>
				<hr>
				<?=clean_html($row['content'])?>
			</div>
		</div>
	</div>
	
<?php
	include(__TEMPLATE__ . 'tail.php');
?>
