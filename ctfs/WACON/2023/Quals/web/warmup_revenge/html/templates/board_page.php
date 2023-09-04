<?php
	if(!defined('__MAIN__')) exit('!^_^!');
	include(__TEMPLATE__ . 'head.php');

	$rows = fetch_multi_row('board', '', '', '0, 15', 'idx DESC');
?>
	<style type="text/css">
		td, th {
			text-align: center;
		}
	</style>
	<div class="container">
		<div class="row">
			<div class="col">
				<table border="1">
					<th style="width:100px">#</th>
					<th style="width:700px">Title</th>
					<th style="width:200px">Writer</th>
					<th style="width:200px">Date</th>

					<?php for($i=0; $i<count($rows); $i++){
						$title = mb_substr($rows[$i]['title'], 0, 30) . '...';
					?>
					<tr>
						<td><?=$rows[$i]['idx']?></td>
						<td><a id='article_<?=$i?>' href="./board.php?p=read&idx=<?=$rows[$i]['idx']?>"><?=clean_html($title)?></a></td>
						<td><?=$rows[$i]['username']?></td>
						<td><?=$rows[$i]['date']?></td>
					</tr>
					<?php } ?>
				</table>
			</div>
		</div>
		<div class="row">
			<div class="col">
				<button type="button" id="write" style="margin-top: 10px" class="btn btn-primary">Write article</button>
			</div>
		</div>
	</div>
	<script src="./static/javascript/write.js"></script>
<?php
	include(__TEMPLATE__ . 'tail.php');
?>

