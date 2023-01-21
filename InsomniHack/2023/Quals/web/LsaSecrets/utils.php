<?php
function generateRandomString($length = 10) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[mt_rand(0, $charactersLength - 1)];
    }
    return $randomString;
}

/** Mysql part **/
function mysqlConnect(){
    $link = new mysqli('db', 'secretsdumpAsService', 'jtfAV4SBkVgFueiWHcRggnRgmR66ncbZaRHtSB')
    or die('Could not connect: ' . mysql_error());
    $link -> select_db('secretsdumpAsService') or die('Could not select database');
    return $link;
}

function mysqlDisconnect($link){
    $link -> close();
}

function checkPassword($link, $password){
    $query = 'SELECT Password FROM passwords where password="'.$password.'" LIMIT 1;';
$result = $link -> query($query) or die('Query failed: ' . mysql_error());
return $result;
}

?>
