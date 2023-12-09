<?php
// Page init hooks
register_init_hook($check_auth, [$_SESSION]);
register_init_hook($check_admin, [$_SESSION]);
register_init_hook($check_request_method, [$_POST]);
execute_init_hooks();

// Logic handling
$exception_handler = fn() => false;

$handle_post_create = fn(&$mysqli) =>
($stmt = $mysqli->prepare('INSERT INTO numbers(num, pipeline, user_id, processed) VALUES(?,?,?,0)')) &&
$stmt->bind_param("ssi", $_POST['num'], $_POST['pipeline'], $_SESSION['id']) &&
($res = $stmt->execute() ?
    set_user_hook('number_added')
    : set_user_hook('something_wrong')
) || header("Refresh:0") || exit();

$handle_post_process = fn(&$mysqli) =>
($stmt = $mysqli->prepare('SELECT id, num, pipeline FROM numbers WHERE user_id = ? AND id = ?')) &&
$stmt->bind_param("ii", $_SESSION['id'], $_POST['id']) &&
$stmt->bind_result($id, $num, $pipeline) &&
(
    ($res = $stmt->execute()) &&
    $stmt->fetch() &&
    ($pipeline_e = explode("\n", $pipeline)) &&
    ($_SESSION['pipeline']['instructions'] = array_map($parse_instruction, $pipeline_e)) &&
    (($_SESSION['pipeline']['num'] = $parse_number($num)) || $_SESSION['pipeline']['num'] == 0) &&
    ($_SESSION['pipeline']['id'] = $id) ?
    set_user_hook('start_processing')
    : set_user_hook('something_wrong')
) || header('Refresh:0') || exit();

$handle_post_delete = fn(&$mysqli) =>
($stmt = $mysqli->prepare('DELETE FROM numbers WHERE user_id = ? AND id = ?')) &&
$stmt->bind_param("ii", $_SESSION['id'], $_POST['id']) &&
($res = $stmt->execute() ?
    false
    : set_user_hook('something_wrong')
) || header("Refresh:0") || exit();

// Internal routing
if ($_POST['_METHOD'] == 'PUT' && isset($_POST['num']) && isset($_POST['pipeline'])) {
    $handle_post_create($mysqli);
}

if ($_POST['_METHOD'] == 'POST' && $_POST['submit'] == 'Process' && isset($_POST['id'])) {
    $handle_post_process($mysqli);
}

if ($_POST['_METHOD'] == 'POST' && $_POST['submit'] == 'Delete' && isset($_POST['id'])) {
    $handle_post_delete($mysqli);
}

// Render function
$render = fn() => print("There's something wrong if you read this.");
