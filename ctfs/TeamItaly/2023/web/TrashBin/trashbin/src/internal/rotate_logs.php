<?php

preg_match('|/b/([^?]*)|', $_SERVER['REQUEST_URI'], $re);
$__BIN_ID = $re[1];
if (str_ends_with($__BIN_ID, '/')) {
	$__BIN_ID = substr($__BIN_ID, 0, -1);
}

$logs = [];
if (!file_exists(__DIR__ . '/../data/' . $__BIN_ID)) {
	http_response_code(500);
	die;
}
$data = file_get_contents(__DIR__ . '/../data/' . $__BIN_ID);
$logs = explode("****", $data);
file_put_contents(__DIR__ . '/../data/' . $__BIN_ID, implode("****", array_slice($logs, max(0, count($logs) - 20), 20)));
