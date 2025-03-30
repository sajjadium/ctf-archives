<?php
chdir('/srv/files');
header('Content-Type: text/plain');
$file = filter_input(INPUT_GET, 'file', FILTER_CALLBACK, ["options"=> function($input) { 
    if (!isset($input)) {
        return null;
    } else if (empty($input)) {
        return false;
    }

    // Sanitize input
    // Remove double dots
    $input = preg_replace('/\.{2,}/', '.', $input);

    // Fail if attempting direct file access
    if (str_starts_with($input, '/')) {
        http_response_code(403);
        exit(0);
    }

    return $input;
}]);

if (!empty($file)) {
    if (!@include_once($file)) {
        echo "File " . htmlspecialchars($file) . " not found!";
    }
} else {
    echo "No file provided.";
}
