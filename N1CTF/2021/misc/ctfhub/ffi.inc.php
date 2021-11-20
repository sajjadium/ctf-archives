<?php
function pstr2ffi(string $str){
    $len=intval((strlen($str)+7)/8);
    if($len>600) die("oom");
    $obj=FFI::new("unsigned long long[".strval($len)."]",false,true);
    FFI::memcpy($obj,$str,$len*8);
    return $obj;
}
function creatbuf($size){
	$size=intval($size);
	if($size<=0) die("oom");
    if($size>4800) die("oom");
    $len=intval(($size+7)/8);
    return FFI::new("unsigned long long[".strval($len)."]",false,true);
}
function releasestr($str){
    FFI::free($str);
}
function getstr($x,$len){
    return FFI::string($x,$len);
}
function encrypt_impl($in,$blks,$key,$out){
if($blks>300) die("too many data");
    FFI::scope("crypt")->encrypt($in,$blks,$key,$out);
}
function decrypt_impl($in,$blks,$key,$out){
if($blks>300) die("too many data");
    FFI::scope("crypt")->decrypt($in,$blks,$key,$out);
}
?>
