<?php
// Page init hooks
register_init_hook($check_not_auth, [$_SESSION]);
register_init_hook($check_request_method, [$_POST]);
execute_init_hooks();

// Logic handling
$exception_handler = fn() => false;

$handle_put = fn(&$mysqli) =>
($stmt = $mysqli->prepare('INSERT INTO users (username, password, is_admin) VALUES(?, ?, false)')) &&
$stmt->bind_param("ss", $_POST['username'], $_POST['password']) &&
(
    ($res = $stmt->execute()) ?
    // Add my fav number to your account <3
    ($stmt = $mysqli->query("INSERT INTO numbers(num, pipeline, user_id, processed, processed_date) VALUES('E','',$mysqli->insert_id,1, NOW())")) &&
    set_user_hook('registration_success') ||
    header("Location: /login")
    : set_user_hook('registration_failure') ||
    header("Location: /register")
) || exit();

$handle_post = fn(&$mysqli) =>
($stmt = $mysqli->prepare('SELECT * FROM users WHERE username = ? AND password = ? LIMIT 1')) &&
$stmt->bind_param("ss", $_POST['username'], $_POST['password']) &&
$stmt->bind_result($id, $user, $pass, $admin) &&
set_exception_handler($exception_handler) ||
(
    ($res = $stmt->execute()) &&
    $stmt->fetch() ?
    ($_SESSION['id'] = $id) &&
    ($_SESSION['username'] = $user) &&
    (($_SESSION['admin'] = $admin) ?
        set_user_hook('greet_admin')
        : set_user_hook('login_success')
    ) ||
    header('Location: /home')
    : set_user_hook('login_failure') ||
    header("Location: /login"))
|| exit();

// Internal routing
if ($_POST['_METHOD'] == 'PUT' && isset($_POST['username']) && isset($_POST['password'])) {
    $handle_put($mysqli);
}

if ($_POST['_METHOD'] == 'POST' && isset($_POST['username']) && isset($_POST['password'])) {
    $handle_post($mysqli);
}

// Render function
$render = fn() => print("There's something wrong if you read this.");
