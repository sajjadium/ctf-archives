<?php 
  error_reporting(0);
    include('header2.php');
    include('session.php');
   
   
 
      $con_id=$_POST['con_id'];
   $s_result_id=$_POST['s_result_id'];
  $event_id=$_POST['event_id'];
   $judge_id=$_POST['judge_id'];
  $rankingx=$_POST['rankingx'];
  
  
   
    $conn->query("update sub_results set rank='$rankingx' where subresult_id='$s_result_id'");
    
     
    
   ?>
    
    
<script>
window.location = 'view_score_sheet.php?event_id=<?php echo $event_id ; ?>&judge_id=<?php echo $judge_id; ?>';
alert('alert!');						
</script>

 
 


 