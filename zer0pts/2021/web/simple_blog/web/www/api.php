<?php
header('Content-Type: application/javascript');
$callback = $_GET['callback'] ?? 'render';
if (strlen($callback) > 20) {
  die('throw new Error("callback name is too long")');
}
echo $callback . '(' . json_encode([
  ["id" => 1, "title" => "Hello, world!", "content" => "Welcome to my blog platform!"],
  ["id" => 2, "title" => "Lorem ipsum", "content" => "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."]
]) . ')';