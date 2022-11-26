<?php 

$pdo = new PDO("mysql:host=database;dbname=yeeclass", "yeeclass", "yeeclass");

$username = "flagholder";
$password = base64_encode(random_bytes(40));

echo "Username: $username; Password: $password\n";

// create user
$user_query = $pdo->prepare("INSERT INTO user (username, `password`, class) VALUES (?, ?, ?)");
$user_query->execute(array($username, hash("md5", $password), 0));

// submit flag
$id = uniqid($username."_");
echo $id."\n";

$submit_query = $pdo->prepare("INSERT INTO submission (`hash`, userid, homeworkid, score, content) VALUES (?, ?, ?, ?, ?)");
$submit_query->execute(array(
    hash("sha1", $id),
    $pdo->lastInsertId(),
    1,
    100,
    $_ENV["FLAG"]
));

?>