<?php

require_once __DIR__ . '/db.php';
$pdo = connectToDatabase();

if (!isset($_POST['username'])) {
    http_response_code(400);
    die;
}

$username = trim($_POST['username']);
if (strlen($username) < 5) {
    header('Location: /?error');
    die;
}

$uuid = \Ramsey\Uuid\Uuid::uuid4();
$uuid = $uuid->toString();

try {
    $pdo->beginTransaction();
    $stmt = $pdo->prepare('INSERT INTO `bin` (`id`, `owner`) VALUES (?, ?)');
    $stmt->execute([$uuid, $username]);
    $pdo->commit();
} catch (Exception $e) {
    $pdo->rollBack();
    http_response_code(500);
    die;
}

$_SESSION['id'] = $uuid;
$_SESSION['username'] = $username;
$_SESSION['demo'] = true;
header('Location: /m/' . $uuid);
