<?php
	if(!defined('__MAIN__')) exit('!^_^!');

	include(__TEMPLATE__ . 'head.php');
?>
	<div class="container">
		<div class="row">
			<div class="col">
				<form method="POST" action="">
					<div class="form-group">
						<input class="form-control" type="text" value="<?=clean_html($_SESSION['username']) ?>" readonly>
					</div>
					<div class="form-group">
						<input class="form-control" type="text" value="<?=clean_html($_SESSION['email']) ?>" readonly>
					</div>
					<div class="form-group">
						<input type="password" name="pw" class="form-control" id="exampleInputPassword1" placeholder="Password">
					</div>
					<div class="form-group">
						<input class="form-control" type="text" value="<?=clean_html($_SESSION['level']) ?>" readonly>
					</div>
					<div class="form-group">
						<textarea class="form-control" name="profilebio" id="profilebio"><?= isset($_SESSION['profilebio']) ? clean_html($_SESSION['profilebio']) : '';?></textarea>
					</div>
					<div class="form-check">
						<input class="form-check-input" name="note" type="checkbox" value="enable" id="defaultCheck1" <?=$_SESSION['is_note'] === '1' ? 'checked' : '';?>>
						<label class="form-check-label" for="defaultCheck1">
							Allow Note
						</label>
					</div>
					<div class="form-check">
						<input class="form-check-input" name="temp_save" type="checkbox" value="yes" id="defaultCheck1">
						<label class="form-check-label" for="defaultCheck1">
						Temporary save
						</label>
					</div>
					<div class="form-group" style="margin-top: 10px">
						<button type="submit" class="btn btn-primary">Edit info</button>
					</div>
				</form>
			</div>
		</div>
	</div>
	
<?php
	include(__TEMPLATE__ . 'tail.php');
?>
