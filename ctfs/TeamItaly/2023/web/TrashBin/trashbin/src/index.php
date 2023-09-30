<?php

require_once __DIR__ . '/../vendor/autoload.php';

session_start();

$__full_path = 'http://' . $_SERVER['SERVER_NAME'] . $_SERVER['REQUEST_URI'];
$__parsed_path = parse_url($__full_path);

if ($__parsed_path['path'] === '/') {
	if ($_SERVER['REQUEST_METHOD'] === 'GET') {
		include __DIR__ . '/internal/get_home.php';
	} else if ($_SERVER['REQUEST_METHOD'] === 'POST') {
		include __DIR__ . '/internal/post_home.php';
	} else {
		http_response_code(405);
		die;
	}
} else if (!!preg_match('|^/b/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/?$|', $__parsed_path['path'])) {
	include __DIR__ . '/internal/bin_dump.php';
	if ($_SESSION['demo']) {
		include __DIR__ . '/internal/rotate_logs.php';
	}
} else if (!!preg_match('|^/m/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(/([^?/]+))?/?$|', $__parsed_path['path'])) {
	include __DIR__ . '/internal/manage.php';
} else {
	http_response_code(404);
}
