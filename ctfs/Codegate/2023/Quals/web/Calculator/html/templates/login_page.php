<?php
	if(!defined("__MAIN__")) exit("!^_^!");

	include(__TEMPLATE__ . "head.php");
?>
	<div class="container">
		<div class="row">
			<div class="col">
				<form method="POST" action="">
					<div class="form-group">
						<input class="form-control" id="username" type="text" name="username">
					</div>
					<div class="form-group">
						<input class="form-control" id="password" type="password" name="pw">
					</div>
					<div class="form-group" style="margin-top: 10px">
						<button type="submit" id="submitBtn" class="btn btn-primary">Login</button>
					</div>
				</form>
			</div>
		</div>
	</div>
	
<?php
	include(__TEMPLATE__ . "tail.php");
?>
