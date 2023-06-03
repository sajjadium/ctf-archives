<?php
$db = new SQLite3("/srv/app/dbs/hashes.db");
$token = getenv('JWT_SECRET');
?>