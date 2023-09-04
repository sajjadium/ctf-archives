<?php
	include('./config.php');

	if(!is_login()) die('Plz Login');

	$page_list = array('write', 'read', 'delete');
	if($_POST){
		$page = trim($_GET['p']);

		if(!in_array($page, $page_list)) die('Error occurred');

		if($page === 'write'){
			$require_params = array('to', 'content');

			foreach ($require_params as $key) {
				if(!trim($_POST[$key])) die('Empty value provided');

				$$key = $_POST[$key];
			}

			if(!valid_str($to, 'username')) die('Invalid Value');

			$find = fetch_row('user', array('username'=>$to));

			if(!$find) die('User doesn\'t exist');
			if($find['is_note'] !== '1') die('Receiver has disabled the note');

			$insert = array(
				'idx' => time() . rand(),
				'to_id' => $to,
				'from_id' => $_SESSION['username'],
				'content' => $content,
				'date' => now()
			);
			if(!insert('note', $insert)) die('Error');

			die('Success');
		}
		exit;	
	}

	switch (trim($_GET['p'])) {
		case 'write':
			render_page('note_write');
			break;
		case 'read':
			render_page('note_read');
			break;
		case 'delete':
			if(!trim($_GET['idx'])) die('Not Found');

			$query = array(
				'idx' => trim($_GET['idx']),
				'to_id' => $_SESSION['username']
			);

			if(!fetch_row('note', $query, 'and')) die('Not Found');
			if(!delete('note', $query, 'and')) die('Delete Fail');

			die('Success');

			break;
		default:
			render_page('note');
			break;
	}
	
?>