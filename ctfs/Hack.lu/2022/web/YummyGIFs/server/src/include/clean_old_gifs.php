<?php
/* NOT PART OF THE CHALLENGE, just preventing DOS */

include 'DB.php';
DB::buildMySQL();
$db = DB::getInstance();

$res = $db->query('SELECT random_id, name FROM gifs WHERE user_id != 1 AND timestamp < UTC_TIMESTAMP() - INTERVAL 15 MINUTE');
while($row = $res->fetch_assoc()) {
  try {
  unlink(__DIR__ . '/../uploads/' . $row['random_id'] . '/' . $row['name']);
  rmdir(__DIR__ . '/../uploads/' . $row['random_id']);
  
  $stmt = $db->prepare('DELETE FROM gifs WHERE random_id = ?');
  $stmt->bind_param('s', $row['random_id']);
  $stmt->execute();
  echo 'Deleted ' . $row['random_id'] . '/' . $row['name'] . "\n";
  } catch (Exception $e) {
    echo $e->getMessage();
  }
}