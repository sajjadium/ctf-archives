<?php
//flag in flag
//Attempt to upload failed, you have to start over
if (!isset($_GET['shell']) || !isset($_GET['filename'])) {
    highlight_file(__FILE__);
    die();
}
$shell = $_GET['shell'];
if (preg_match('/(on|flag|index|cat|file)/i', $shell)) {
    die("Try hard broooooo !!!");
}
$filename = $_GET['filename'];
if (preg_match("/[^a-z.]/", $filename)) {
    die("Try hard broooooo !!!");
}

file_put_contents($filename, $shell . "\nWelcome to ISITDTU CTF 2022");
?>