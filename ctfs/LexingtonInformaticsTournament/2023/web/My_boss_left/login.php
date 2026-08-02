<?php
// Check if the request is a POST request
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Read and decode the JSON data from the request body
    $json_data = file_get_contents('php://input');
    $login_data = json_decode($json_data, true);

    // Replace these values with your actual login credentials
    $valid_password = 'dGhpcyBpcyBzb21lIGdpYmJlcmlzaCB0ZXh0IHBhc3N3b3Jk';

    // Validate the login information
    if ($login_data['password'] == $valid_password) {
        // Login successful
        echo json_encode(['status' => 'success', 'message' => 'LITCTF{redacted}']);
    } else {
        // Login failed
        echo json_encode(['status' => 'error', 'message' => 'Invalid username or password']);
    }
}
?>
