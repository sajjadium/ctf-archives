<?php
	include('./config.php');

	if(!is_login()) die("Login Plz");

	if($_POST){
		$page = trim($_GET['p']);
		
		if($page === 'write'){
			
			$insert = array();

			$require_params = array('title', 'content', 'level', 'password');
			foreach ($require_params as $key) {
				if(!trim($_POST[$key])) die('Empty value provided');

				$$key = $_POST[$key];
			}

			if(mb_strlen($title) > 200 || mb_strlen($content) > 200) die('Too Long');
 			if(intval($_SESSION['level']) < intval($level)) die('You cannot set a value above your level');

 			$insert['title'] = $title;
 			$insert['content'] = $content;
 			$insert['username'] = $_SESSION['username'];
			$insert['require_level'] = $level;
			$insert['date'] = now();
			$insert['password'] = md5($password);

			if($_FILES['file']['tmp_name']){
				if($_FILES['file']['size'] > 2097152){
					die('File is too big');
				}
				$file_name = bin2hex(random_bytes(30));

				if(!move_uploaded_file($_FILES['file']['tmp_name'], './upload/' . $file_name)) die('Upload Fail');

				$insert['file_path'] = './upload/' . $file_name;
				$insert['file_name'] = $_FILES['file']['name'];
			}

			if(!insert('board', $insert)) die('Fail');

			$replace = array('point' => intval($_SESSION['point']) + 1);
			$query   = array('username' => $_SESSION['username']);

			if(!update('user', $replace, $query)) die('Error');

			$_SESSION['point'] = intval($_SESSION['point']) + 1;

			die('Success');
		}
		exit;
	}
	switch (trim($_GET['p'])){
		case 'write':
			render_page('article_write');
			break;
		case 'delete':
			if(!trim($_GET['idx'])) die('Not Found');

			$query = array(
				'idx' => trim($_GET['idx']),
				'username' => $_SESSION['username']
			);

			if(!fetch_row('board', $query, 'and')) die('Not Found');
			if(!delete('board', $query, 'and')) die('Delete failed');

			die('Success');

			break;
		case 'read':
			render_page('article_read');
			break;
		default:
			render_page('board');
			break;
	}
	
?>