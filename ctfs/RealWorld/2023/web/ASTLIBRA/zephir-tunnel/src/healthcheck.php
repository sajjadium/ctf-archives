<?php
require_once('config.php');
function check_db(){
    global $dbc;
    $query = "SELECT count(*) FROM jobs WHERE checked = 0";
    $stmt = $dbc->prepare($query);
    $stmt->execute();
    $result = $stmt->get_result();
    $row = $result->fetch_assoc();
    if($row['count(*)'] <= 10){
        return true;
    }
    return false;
    
}
function check_bot(){
    $file = "/var/tmp/succ";
    if(file_exists($file)){
        $mtime = filemtime($file);
        if(time() - $mtime > 120){
            return false;
        }
        else{
            return true;
        }
    } else {
        return false;
    }
}

if(check_db() && check_bot()){
    echo json_encode(array("status" => "success", "message" => "OK"));
} else {
    echo json_encode(array("status" => "error", "message" => "Bot or db is not working"));
}