<?php
session_start();
$host = 'db';
$username = 'root';
$password = 'realworldctf';
$database = 'web';
$dbc = mysqli_connect($host, $username, $password, $database);

if (!$dbc){
    echo json_encode(array("status" => "error", "message" => "Database connection failed"));
    exit();
}
$dbc->query("SET NAMES utf8mb4");
$tmpl = <<<ZEPF
namespace {namespace};

class {class}{
    public function getURL(){
        return "{base64url}";
    }
    public function test(){
        var ch = curl_init();
        curl_setopt(ch, CURLOPT_URL, "{url}");
        curl_setopt(ch, CURLOPT_HEADER, 0);
        curl_exec(ch);
        curl_close(ch);
        return true;
    }
}
ZEPF;

function job_exists($class){
    global $dbc;
    $query = "SELECT * FROM jobs WHERE checked = 0 and `class` = ?";
    $stmt = $dbc->prepare($query);
    $stmt->bind_param("s", $class);
    $stmt->execute();
    $result = $stmt->get_result();
    if($result->num_rows > 0){
        return true;
    }
    return false;
}

function add_job($zep_file, $namespace, $class){
    global $dbc;
    $query = "INSERT INTO jobs (zep_file, `namespace`, `class`, checked, result) VALUES (?, ?, ?, ?, ?)";
    $stmt = $dbc->prepare($query);
    $checked = 0;
    $result = "";
    $stmt->bind_param("sssis", $zep_file, $namespace, $class, $checked, $result);
    $stmt->execute();
}

function wait_for_result($class){
    global $dbc;
    $query = "SELECT * FROM jobs WHERE `class` = ? limit 1";
    $stmt = $dbc->prepare($query);
    $stmt->bind_param("s", $class);
    $stmt->execute();
    $result = $stmt->get_result();
    $row = $result->fetch_assoc();
    while($row['checked'] == 0){
        sleep(1);
        $stmt->execute();
        $result = $stmt->get_result();
        $row = $result->fetch_assoc();
    }
    $res = $row['result'];
    $query = "DELETE FROM jobs WHERE id = ?";
    $stmt = $dbc->prepare($query);
    $stmt->bind_param("i", $row['id']);
    $stmt->execute();
    return $res;
}

function generateRandomString($length = 10) {
    $characters = 'abcdefghijklmnopqrstuvwxyz';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomString;
}

?>