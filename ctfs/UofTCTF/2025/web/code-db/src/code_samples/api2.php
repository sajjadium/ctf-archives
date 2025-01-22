<?php
header('Content-Type: application/json');
$method = $_SERVER['REQUEST_METHOD'];
$uri = $_SERVER['REQUEST_URI'];

$users = [
    1 => ['name' => 'Alice', 'email' => 'alice@example.com'],
    2 => ['name' => 'Bob', 'email' => 'bob@example.com'],
];

switch ($method) {
    case 'GET':
        echo json_encode($users);
        break;
    case 'POST':
        $input = json_decode(file_get_contents('php://input'), true);
        $id = max(array_keys($users)) + 1;
        $users[$id] = $input;
        echo json_encode($users[$id]);
        break;
    case 'PUT':
        parse_str(file_get_contents("php://input"), $put_vars);
        $id = $put_vars['id'];
        if(isset($users[$id])){
            $users[$id] = array_merge($users[$id], $put_vars);
            echo json_encode($users[$id]);
        } else {
            echo json_encode(['error' => 'User not found']);
        }
        break;
    case 'DELETE':
        parse_str(file_get_contents("php://input"), $delete_vars);
        $id = $delete_vars['id'];
        if(isset($users[$id])){
            unset($users[$id]);
            echo json_encode(['message' => 'User deleted']);
        } else {
            echo json_encode(['error' => 'User not found']);
        }
        break;
    default:
        echo json_encode(['error' => 'Invalid request method']);
        break;
}
?>
