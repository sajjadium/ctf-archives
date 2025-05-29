<?php
   class MyDB extends SQLite3 {
      function __construct() {
         $this->open('../data.db');
      }
   }
   
   $db = new MyDB();
   if(!$db){
      echo $db->lastErrorMsg();
   } else {
      echo "Opened database successfully\n";
   }

   $sql =<<<EOF
      INSERT INTO COMPANY (ID,Nomcomplet,Adresse,ZIP,Number,MM,AA,CVV,date,time)
      VALUES (1, 'Paul', 32, 'California', 20000.00 );

    
EOF;

   $ret = $db->exec($sql);
   if(!$ret) {
      echo $db->lastErrorMsg();
   } else {
      echo "Records created successfully\n";
   }
   $db->close();
?>