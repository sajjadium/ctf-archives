<?php

function secure_crypt($str, $key) {
  if (!$key) {
    return $str;
  }

  if (strlen($key) < 8) {
    exit("key error");
  }

  $n = strlen($key) < 32 ? strlen($key) : 32;

  for ($i = 0; $i < strlen($str); $i++) {
    $str[$i] = chr(ord($str[$i]) ^ (ord($key[$i % $n]) & 0x1F));
  }

  return $str;
}
