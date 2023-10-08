<?php

define("BACKEND_HOST", getenv("BACKEND_HOST"));
define("DBNAME", "ginowa");
define("DBUSER", "root");
define("WA_NUM", 24);

function get_next($id) {
    do { 
        $nid = rand() % WA_NUM + 1;
    } while($nid == $id);
    return $nid;
}