<?php
include("config.php");

$host = DBHOST; 
$dbname = DBNAME;
$username = DBUSER;
$password = DBPASS;

if(isset($_GET['id']))
    $id = $_GET['id'];
else
    $id = '1';

$ret = [];
$conn = new mysqli($host, $username, $password, $dbname);
if ($conn->connect_error) {
    $ret["status"] = "error";
} else {
    $conn->set_charset("utf8");
    $stmt = $conn->prepare("SELECT 'ok' AS status, name, age, url FROM info WHERE id = '" . $id . "'");
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $res = $result->fetch_assoc();
        $ret["status"] = $res["status"];
        $ret["name"] = $res["name"];
        $ret["age"] = $res["age"];
        $ret["url"] = $res["url"];
    } else {
        $ret["status"] = "error";
    }
}
header('Content-Type: application/json');
echo json_encode($ret);
?>

