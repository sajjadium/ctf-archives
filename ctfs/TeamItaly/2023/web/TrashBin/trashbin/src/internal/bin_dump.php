<?php

require_once __DIR__ . '/db.php';
$pdo = connectToDatabase();

preg_match('|/b/([^?]*)|', $_SERVER['REQUEST_URI'], $re);
$__BIN_ID = $re[1];
if (str_ends_with($__BIN_ID, '/')) {
	$__BIN_ID = substr($__BIN_ID, 0, -1);
}

function getBinInfo()
{
	global $pdo, $__BIN_ID;
	try {
		$stmt = $pdo->prepare("SELECT * FROM `bin` WHERE `id`=?");
		$stmt->execute([$__BIN_ID]);
		$data = $stmt->fetchAll();
		if (count($data) !== 1) {
			http_response_code(404);
			die;
		}
		return $data[0];
	} catch (Exception $e) {
		http_response_code(500);
		die;
	}
}

$bin = getBinInfo();

$method = $_SERVER['REQUEST_METHOD'];

$__full_path = 'http://' . $_SERVER['SERVER_NAME'] . $_SERVER['REQUEST_URI'];
$__parsed_path = parse_url($__full_path);
$path = substr($__parsed_path['path'], 39);
if (!str_starts_with($path, '/')) {
	$path = '/' . $path;
}

if (isset($__parsed_path['query']))
	parse_str($__parsed_path['query'], $query);

$headers = getallheaders();
$raw_body = file_get_contents('php://input');

$form = $_POST;
$cookies = $_COOKIE;

$uuid = \Ramsey\Uuid\Uuid::uuid4();
$uuid = $uuid->toString();

$dump = base64_encode(json_encode([
	'id' => $uuid,
	'method' => $method,
	'path' => $path,
	'raw_path' => $path . (isset($__parsed_path['query']) ? '?' . $__parsed_path['query'] : ''),
	'query' => $query,
	'headers' => $headers,
	'raw_body' => $raw_body,
	'form' => $form,
	'cookies' => $cookies,
	'time' => time()
]));

function template($in)
{
	$matches = [];
	$substitutions = [];
	preg_match_all('/\$\{GET\[([\w-]+)\]\}/', $in, $re);
	foreach ($re[1] as $key) {
		if (array_search("\${GET[$key]}", $matches) === false) {
			$matches[] = "\${GET[$key]}";
			$substitutions[] = isset($_GET) ? $_GET[$key] ?? '' : '';
		}
	}

	preg_match_all('/\$\{POST\[([\w-]+)\]\}/', $in, $re);
	foreach ($re[1] as $key) {
		if (array_search("\${POST[$key]}", $matches) === false) {
			$matches[] = "\${POST[$key]}";
			$substitutions[] = isset($_POST) ? $_POST[$key] ?? '' : '';
		}
	}

	preg_match_all('/\$\{COOKIE\[([\w-]+)\]\}/', $in, $re);
	foreach ($re[1] as $key) {
		if (array_search("\${COOKIE[$key]}", $matches) === false) {
			$matches[] = "\${COOKIE[$key]}";
			$substitutions[] = isset($_COOKIE) ? $_COOKIE[$key] ?? '' : '';
		}
	}

	preg_match_all('/\$\{HEADER\[([\w-]+)\]\}/', $in, $re);
	foreach ($re[1] as $key) {
		if (array_search("\${HEADER[$key]}", $matches) === false) {
			$matches[] = "\${HEADER[$key]}";
			$substitutions[] = isset($headers) ? $headers[$key] ?? '' : '';
		}
	}

	return str_replace($matches, $substitutions, $in);
}

// read old logs
$logs = [];
if (file_exists(__DIR__ . '/../data/' . $__BIN_ID)) {
	$data = file_get_contents(__DIR__ . '/../data/' . $__BIN_ID);
	$logs = explode("****", $data);
}
// append new logs
$logs[] = $dump;
// write to file
file_put_contents(__DIR__ . '/../data/' . $__BIN_ID, implode("****", $logs));

// Response headers
header('Access-Control-Allow-Origin: *');
$response_headers = json_decode($bin['response_headers']);
foreach ($response_headers as $key => $value) {
	header($key . ': ' . template($value));
}

// Response text
echo template($bin['response_text']);

if (!$_SESSION['demo'] && $bin['forward_request'] && !!$bin['forward_request_url']) {
	$client = new \GuzzleHttp\Client();
	$method = 'get';
	if (!!$bin['forward_request_body']) {
		$method = 'post';
	}
	$client->$method($bin['forward_request_url'], [
		'headers' => array_map(fn ($x) => template($x), (array) json_decode($bin['forward_request_headers'])),
		'body' => !!$bin['forward_request_body'] ? template($bin['forward_request_body']) : NULL
	]);
}
