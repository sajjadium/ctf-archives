<?php
    $db = new PDO('sqlite:/tmp/leakynote.db');
    $db->exec("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT);");
    $db->exec("CREATE TABLE IF NOT EXISTS posts (username TEXT, id TEXT, title TEXT, contents TEXT);");

    // check for admin user
    $stmt = $db->prepare("SELECT * FROM users WHERE username=?");
    $stmt->execute(["admin"]);
    $user = $stmt->fetch();

    if (!$user) {
        // initialize admin user
        $admin_password = getenv("ADMIN_PASSWORD") ?: "admin_password";
        $hash = password_hash($admin_password, PASSWORD_BCRYPT);
        $stmt = $db->prepare("INSERT INTO users (username, password) VALUES (?, ?)");
        $stmt->execute(["admin", $hash]);
        // initialize flag post
        $stmt = $db->prepare("INSERT INTO posts (username, id, title, contents) VALUES (?, ?, ?, ?)");
        $stmt->execute(["admin", bin2hex(random_bytes(8)), "flag", getenv("FLAG") ?: "corctf{test_flag}"]);
    }
?>