<?php 
 
    include('header2.php');
    include('session.php');
    
 
 
 
    $status=$_GET['status'];
    $se_name=$_GET['se_name'];
    $sub_event_id=$_GET['sub_event_id'];
    
    
    
    
 
  if($status=="activated")
  {
 
    $conn->query("update sub_event set status='deactivated' where subevent_id='$sub_event_id'");?>
    
    
                <script>
                window.location = 'home.php';
                alert('Sub-Event:<?php echo $se_name; ?> deactivated successfully!');						
                </script>


<?php }else{
    
$conn->query("update sub_event set status='activated' where subevent_id='$sub_event_id'");

$cont_query = $conn->query("SELECT * FROM contestants WHERE subevent_id='$sub_event_id'") or die(mysql_error());
if($cont_query->rowCount()>0)
{
    ?>
                <script>
                alert('Sub-Event:<?php echo $se_name; ?> activated successfully!');	
                window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id; ?>&se_name=<?php echo $se_name; ?>';				
                </script>

  <?php
    
}
else
{
  ?>
                <script>
                alert('Sub-Event:<?php echo $se_name; ?> activated successfully!');	
                window.location = 'sub_event_details.php?sub_event_id=<?php echo $sub_event_id; ?>&se_name=<?php echo $se_name; ?>';				
                </script>

  <?php  } }?>