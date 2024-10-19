<?php
include('dbcon.php');
include('session.php');

$org_pass = $_POST['org_pass'];

 if($check_pass==$org_pass){
    
 

    $id=$_POST['selector'];

    $N = count($id);
    for($i=0; $i < $N; $i++)
    {
 $conn->query("delete from contestants where contestant_id='$id[$i]'"); 
    }

 

  ?>
	<script>window.location = 'sub_event_details_edit.php';
	alert('Client(s) successfully deleted.');</script>
    <?php
}
else
{
      ?>
	<script>window.location = 'sub_event_details_edit.php';
	alert('Confirmation password is invalid!');</script>
    <?php
}
?>
