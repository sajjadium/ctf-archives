<?php
	if(!defined('__MAIN__')) exit('!^_^!');
	include(__TEMPLATE__ . 'head.php');
?>
	<div class="container">
		<div class="row">
			<div class="col">
				<form  action="" method="POST" enctype="multipart/form-data">
					<div class="form-group">
						<input type="text" name="title" class="form-control" placeholder="Title">
					</div>
					<div class="form-group">
						<textarea  name="content" class="form-control" placeholder="Content" rows="10"></textarea>
					</div>
					<div class="form-group">
						<select name="level" class="form-control" id="exampleFormControlSelect1">
							<option value="1">Level 1 or higher</option>
							<option value="2">Level 2 or higher</option>
							<option value="3">Level 3 or higher</option>
							<option value="4">Level 4 or higher</option>
							<option value="5">Level 5 or higher</option>
						</select>
					</div>
					<div class="custom-file">
						<input type="file" class="form-control-file" name="file">
					</div>
					<div class="form-group">
					<input type="text" name="password" class="form-control" placeholder="password">
					</div>
					<button class="btn btn-primary" type="submit" style="margin-top: 10px">Write</button>
				</form>
			</div>
		</div>
	</div>
<?php
	include(__TEMPLATE__ . 'tail.php');
?>

