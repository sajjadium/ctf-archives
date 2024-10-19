<?php


include('db.php');


$check = $conn->query("SELECT * FROM comment order by id desc");
 


if(isset($_POST['content']))
{
$content=$_POST['content'];



 $conn->query("INSERT INTO comment(msg)values('$content')");
  
  
$news_query = $conn->query("SELECT * FROM comment order by id desc");
$row=$news_query->fetch();

                         
}



?>

<div class="showbox"> <?php echo $row['msg']; ?> </div>
