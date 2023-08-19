<?php
include "./config.php";

function err_handler($errno, $msg, $file, $line)
{
	return true;
}
set_error_handler("err_handler");

$resp_time = 3.0;

$start = microtime(true);

if (!isset($_GET['cmd'])) die;

$res = '{"res": "request failed."}';

$cmd = $_GET['cmd'];
switch($cmd) {
	case 'findbyisbn':
		if ((isset($_GET['isbn']) && strlen($_GET['isbn']) >= 10)) {
			$db = dbconnect();
			pg_prepare($db, "find_by_isbn", "SELECT * FROM books WHERE isbn=$1");
			$result = pg_execute($db, "find_by_isbn", array($_GET['isbn']));
			pg_close($db);
			if($result) {
		        $rows = pg_fetch_assoc($result);
				if ($rows) $res = json_encode($rows);
			}
		}
		break;
	case 'requestbook':
		if ((isset($_GET['isbn']) && strlen($_GET['isbn']) >= 10)) {
			$res = '{"res": "Sorry, but our budget is not enough to buy <a href=\'https://isbnsearch.org/isbn/'.$_GET['isbn'].'\'>this book</a>."}';
			$db = dbconnect();
			$result = pg_query($db, "SELECT ISBN FROM books WHERE isbn='".$_GET['isbn']."'");
			pg_close($db);
			if ($result) {
				$rows = pg_fetch_assoc($result);
				if ($rows) {
					$isbn = (int)$rows["isbn"];
					if (($isbn >= 1000000000) && ((string)$isbn === $rows["isbn"]))
					{
						$res = '{"res": "We already have this book('.$rows["isbn"].')."}';
					}
				}
			}
		}
		break;
	default:
		die;
}

$now = microtime(true);

if ($now - $start < $resp_time) {
	usleep((int)(($resp_time + $start - $now) * 1000000));
}

echo $res;

?>
