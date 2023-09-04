<?php
	if(!defined('__MAIN__')) exit('!^_^!');

	include(__TEMPLATE__ . 'head.php');
?>
	<div class="container">
		<div class="row">
			<div class="col">
				<form  action="" method="POST">
					<div class="form-group">
						<input type="text" name="to" class="form-control" placeholder="Receiver">
					</div>
					<div class="form-group">
						<textarea  name="content" class="form-control" placeholder="Content" rows="10"></textarea>
					</div>
					<button class="btn btn-primary" type="submit" style="margin-top: 10px">Send</button>
				</form>
			</div>
		</div>
	</div>
	
<?php
	include(__TEMPLATE__ . 'tail.php');
?>

