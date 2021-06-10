<?php

class posts
{

public function __construct($id)
{
$this->id= $id;
}
public function get_post()
{
require("db/config.php");
$res = $conn->prepare("SELECT content FROM Blog_posts1 WHERE name=?");
if (!($res->bind_param("s",$this->id)) || !($res->execute()) || !($result = $res->get_result()))
	die('Can\'t get your blogs :-(');
if ($result->num_rows > 0) {
	while ($row = $result->fetch_assoc()) {
		echo htmlspecialchars($row["content"], ENT_QUOTES, 'UTF-8');

	}
}
}

public function __destruct()
{
require("db/config.php");
$res = $conn->prepare("SELECT content FROM Blog_posts1 WHERE name=?");
if (!($res->bind_param("s",$this->id)) || !($res->execute()) || !($result = $res->get_result()))
	die('Can\'t get your blogs :-(');
if ($result->num_rows > 0) {
	while ($row = $result->fetch_assoc()) {
		return htmlspecialchars($row["content"], ENT_QUOTES, 'UTF-8');

	}
}
}
}