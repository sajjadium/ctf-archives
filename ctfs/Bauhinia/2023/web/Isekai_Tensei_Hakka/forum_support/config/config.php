<?php

/////////////////////////////////////////////////////////////
// Please note that if you get any errors when connecting, //
// that you will need to email your host as we cannot tell //
// you what your specific values are supposed to be        //
/////////////////////////////////////////////////////////////

// type of database running
// (only mysql is supported at the moment)
$dbservertype='mysql';

// hostname or ip of server
$servername='localhost'; //<--你使用的db的ip或網址

// username and password to log onto db server
$dbusername='root'; //<--連結db的帳號
$dbpassword=''; //<--連結db的密碼

// name of database
$dbname='test123'; //<--你使用的db名稱

// technical email address - any error messages will be emailed here
$technicalemail='me@localhost'; //<--當有error訊息時所要寄發的email位子

// use persistant connections to the database
// 0 = don't use
// 1 = use
$usepconnect=0;

?>