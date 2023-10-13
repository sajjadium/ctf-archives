<?php

function connect_db() {
    $db = new SQLite3('/tmp/stylepen.db');
    return $db;
}

function init_db() {
    $db = connect_db();
    $db->exec('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)');
    $db->exec('CREATE TABLE IF NOT EXISTS submissions (id TEXT PRIMARY KEY, css TEXT, email TEXT, winner BOOLEAN)');

    $pw = getenv("SHARED_SECRET") ?: "secret";
    $adminpw_hash = password_hash($pw, PASSWORD_ARGON2ID);
    $raterpw_hash = password_hash($pw, PASSWORD_ARGON2ID);

    $stmt = $db->prepare('INSERT INTO users (username, password) VALUES (:username, :password)');

    $stmt->bindValue(':username', "admin", SQLITE3_TEXT);
    $stmt->bindValue(':password', $adminpw_hash, SQLITE3_TEXT);
    $stmt->execute();
    $stmt->reset();
    $stmt->bindValue(':username', "rater", SQLITE3_TEXT);
    $stmt->bindValue(':password', $raterpw_hash, SQLITE3_TEXT);
    $stmt->execute();

    $flag = getenv("FLAG") ?: '<style>#flag { color: red; }</style><div id="flag">flag{testflag}</div>';
    insert_submission($flag, "gladstone@gander.com", true);

    $db->close();
}

function insert_submission($css, $email, $winner=false) {
    $db = connect_db();
    $id = bin2hex(random_bytes(16));
    $stmt = $db->prepare('INSERT INTO submissions (id, css, email, winner) VALUES (:id, :css, :email, :winner)');
    $stmt->bindValue(':id', $id, SQLITE3_TEXT);
    $stmt->bindValue(':css', $css, SQLITE3_TEXT);
    $stmt->bindValue(':email', $email, SQLITE3_TEXT);
    $stmt->bindValue(':winner', $winner, SQLITE3_INTEGER);
    $stmt->execute();
    $db->close();
    return $id;
}

function get_submission($id) {
    $db = connect_db();
    $stmt = $db->prepare('SELECT * FROM submissions WHERE id = :id');
    $stmt->bindValue(':id', $id, SQLITE3_TEXT);
    $result = $stmt->execute();
    $row = $result->fetchArray();
    $db->close();
    return $row;
}

function get_winning_submission() {
    $db = connect_db();
    $result = $db->query('SELECT * FROM submissions WHERE winner = 1');
    $row = $result->fetchArray();
    $db->close();
    return $row;
}

function login($username, $password) {
    $db = connect_db();
    $stmt = $db->prepare('SELECT * FROM users WHERE username = :username');
    $stmt->bindValue(':username', $username, SQLITE3_TEXT);
    $result = $stmt->execute();
    $row = $result->fetchArray();
    $db->close();
    if ($row && password_verify($password, $row['password'])) {
        return $row['username'];
    }
    return false;
}

// if db is empty, initialize it
$db = connect_db();
$result = $db->query('SELECT * FROM users');
$db->close();
if ($result === false) {
    init_db();
}