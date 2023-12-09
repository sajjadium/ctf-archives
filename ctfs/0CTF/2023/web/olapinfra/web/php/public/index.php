<?php
error_reporting(E_ALL ^ E_DEPRECATED);
require __DIR__ . '/../vendor/autoload.php';
if (!isset($_GET['query'])) {
  show_source(__FILE__);
  exit;
}
$config = [
  'host' => 'clickhouse',
  'port' => '8123',
  'username' => 'default',
  'password' => ''
];
$db = new ClickHouseDB\Client($config);
$db->database('default');
$db->setTimeout(1.5);
$db->setTimeout(10);
$db->setConnectTimeOut(5);
$db->ping(true);
$statement = $db->select('SELECT * FROM u_data WHERE ' . $_GET['query'] . ' LIMIT 10');
echo (json_encode($statement->rows()));


// Err 'Uncaught ClickHouseDB\Exception\DatabaseException: connect to hive metastore: thrift' or
// Err 'NoSuchObjectException(message=hive.default.u_data table not found)',
// please wait for >= 1min, hive is not initialized.
