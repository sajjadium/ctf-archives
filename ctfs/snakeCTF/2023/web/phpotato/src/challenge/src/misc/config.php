<?php
$mysqli = null;

$define_flag = fn() => define('FLAG', getenv('FLAG'));

$define_db_params = fn() =>
define('DB_HOSTNAME', getenv('DB_HOST')) &&
define('DB_USER', getenv('DB_USER')) &&
define('DB_PASSWORD', getenv('DB_PASSWORD')) &&
define('DB_DATABASE', getenv('DB_DATABASE')) &&
define('DB_PORT', getenv('DB_PORT'));

$define_error_display = fn() =>
MYSQLI_REPORT(MYSQLI_REPORT_OFF) && // Avoid warning breaking redirection..
error_reporting(E_ALL) &&
ini_set('display_errors', 1);

$init_db = fn(&$mysqli) => $mysqli = new mysqli(DB_HOSTNAME, DB_USER, DB_PASSWORD, DB_DATABASE, DB_PORT);

register_init_hook($define_flag);
register_init_hook($define_db_params);
register_init_hook($define_error_display);
register_init_hook($init_db, [ &$mysqli]);

$define_init_params = fn() =>
define('DEFAULT_PRECISION', getenv('PRECISION'));

register_init_hook($define_init_params);

// Register global variables for the router
if (isset($register_global)) {
    $register_global('mysqli');
}
