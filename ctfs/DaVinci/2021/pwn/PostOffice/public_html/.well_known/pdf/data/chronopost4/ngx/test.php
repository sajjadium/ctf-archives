<?php

$zip = new ZipArchive;
$res = $zip->open('data.zip', ZipArchive::CREATE); //Add your file name
if ($res === TRUE) {
   $zip->addFromString('data.txt', 'file content goes here'); //Add your file name
   $zip->setEncryptionName('data.txt', ZipArchive::EM_AES_256, 'PASSWORD'); //Add file name and password dynamically
   $zip->close();
   echo 'ok';
} else {
   echo 'failed';
}