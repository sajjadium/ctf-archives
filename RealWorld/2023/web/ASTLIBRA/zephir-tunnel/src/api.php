<?php
require_once('config.php');
if(!isset($_SESSION["username"])){
    echo json_encode(array("status" => "error", "message" => "Please login first"));
    exit();
}
if(!isset($_POST['URL'])){
    echo json_encode(array("status" => "error", "message" => "URL not set"));
    exit();
}

$username = $_SESSION["username"];
$url = addslashes($_POST['URL']);
if($url[0]!="h" || $url[1]!="t" || $url[2]!="t" || $url[3]!="p"){
    echo json_encode(array("status" => "error", "message" => "Invalid URL"));
    exit();
}
$class = $username;
$namespace = ucfirst($class.generateRandomString(5));
$zep_file = preg_replace('/(.*)\{namespace\}(.*)/is', '${1}'.$namespace.'${2}', $tmpl);
$zep_file = preg_replace('/(.*)\{class\}(.*)/is', '${1}'.$class.'${2}', $zep_file);
$zep_file = preg_replace('/(.*)\{base64url\}(.*)/is', '${1}'.base64_encode($url).'${2}', $zep_file);
$zep_file = preg_replace('/(.*)\{url\}(.*)/is', '${1}'.$url.'${2}', $zep_file);
if(!job_exists($class)){
   add_job($zep_file, $namespace, $class);
}
$result  = wait_for_result($class);
echo json_encode(array("status" => "success", "message" => base64_encode($result)));

?>