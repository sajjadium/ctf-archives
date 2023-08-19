<?php
  function dbconnect(){
    $db=pg_connect("host=db dbname=books user=".$_ENV["DB_USER"]." password=".$_ENV["DB_PWD"]) or die("db connection error");
    return $db;
  }
