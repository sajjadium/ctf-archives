<?php
include 'filter.php';

$r = function($errorno, $errstr, $errfile, $errline) {error_log("[$errorno] $errstr", 0);};
set_error_handler(function() use(&$r){ $r = True; });

if(!isset($_GET['mode'])){
    echo "Welcome!!";
}else if($_GET['mode'] == "chance"){
    if(strlen($_GET['chance']) > 15 | filter($_GET['chance'],1) | checkLetterNums($_GET['chance'])) exit("No Hack T.T");
    eval($_GET['chance']);
}

if(isset($_GET['bonus'])){
    if(strlen($_GET['bonus']) > 32 | filter($_GET['bonus'])) exit("No bonus ~.~");
    include $_GET['bonus'];
}

?>