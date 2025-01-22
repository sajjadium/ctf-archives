<?php
$method = $_SERVER['REQUEST_METHOD'];

$tasks = [
    ['id' => 1, 'task' => 'Buy groceries'],
    ['id' => 2, 'task' => 'Read a book'],
];

header('Content-Type: application/json');

switch ($method) {
    case 'GET':
        echo json_encode($tasks);
        break;
    case 'POST':
        $input = json_decode(file_get_contents('php://input'), true);
        $newTask = ['id' => time(), 'task' => $input['task']];
        $tasks[] = $newTask;
        echo json_encode($newTask);
        break;
    default:
        echo json_encode(['message' => 'Method not allowed']);
        break;
}
?>
