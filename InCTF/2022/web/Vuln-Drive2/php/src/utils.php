<?php

function check_name($filename){
    if(gettype($filename)==="string"){
        if(preg_match("/[.\/]/i",$filename)){
            report();
            return false;
        }else{
            return true; //safe
        }
    }
    else{
        return false;
    }
}

function report(){
    //report usename
    ini_set("from",$_SESSION['username']);
    file_get_contents('http://localhost/report.php');

}

function upload($filename,$path,$name){
    if(is_dir($path)){
        move_uploaded_file($filename,$path."/".$name);
    }else{
        die("Failed to upload");
    }
}