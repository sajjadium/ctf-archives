<?php

function genRandString($length) {
  $allowable_characters = 'abcdefghijklmnopqrstuvwxyz';
  $len = strlen($allowable_characters) - 1;
  $str = '';

  for ($i = 0; $i < $length; $i++) {
    $str .= $allowable_characters[mt_rand(0, $len)];
  }

  return $str;
}

function genTmpPwd() {
  list($usec, $sec) = explode(' ', microtime());
  $usec *= 1000000;
  $tmpPass = genRandString(8) . $sec . $usec . posix_getpid(); 

  return $tmpPass;
}

function createCsrf() {
  mt_srand();
  return md5(genRandString(8));
}

?>