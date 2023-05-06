<?php
    $con = mysqli_init();
    $key = $_GET['key'];
    $value = $_GET['value'];
    if(strlen($value) > 1500){
        die('too long');
    }
    if (is_numeric($key) && is_string($value)) {
        mysqli_options($con, $key, $value);
    }
    mysqli_options($con, MYSQLI_OPT_LOCAL_INFILE, 0);
    if (!mysqli_real_connect($con, "127.0.0.1", "test", "test123456", "mysql")) {
        $content = 'connect failed';
    } else {
        $content = 'connect success';
    }
    mysqli_close($con);
    echo $content;    
?>
