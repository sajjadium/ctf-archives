<?php 
  error_reporting(0);
    include('header2.php');
    include('session.php');
    
 
 
   $contestant_name=$_POST['contestant_name'];
   $contestant_id=$_POST['contestant_id'];
  $judge_id=$_POST['judge_id'];
   $judge_ctr=$_POST['judge_ctr'];
   $subevent_id=$_POST['subevent_id'];
   $jcomment=$_POST['jcomment'];   
  
  
  $conn->query("update sub_results set judge_rank_stat='' where subevent_id='$subevent_id' AND judge_id='$judge_id'");
  
   
    $cp6=$_POST['cp6'];
   $cp5=$_POST['cp5'];
   $cp4=$_POST['cp4'];
   $cp3=$_POST['cp3'];
   $cp2=$_POST['cp2'];
    $cp1=$_POST['cp1'];
   
   if($cp6=="")
   {
    $cp6="";
     
   if($cp5=="")
   {
    $cp5="";
     
   if($cp4=="")
   {
    $cp4="";
     
   if($cp3=="")
   {
    $cp3="";
    
     if($cp2=="")
   {
    $cp2="";
    }
    else
    {
    $total_score=$cp1+$cp2;
        $conn->query("update sub_results set total_score='$total_score',criteria_ctr1='$cp1',criteria_ctr2='$cp2', comments='$jcomment' where contestant_id='$contestant_id' AND judge_id='$judge_id'");
   }
    
   }
   else
   {
    $total_score=$cp1+$cp2+$cp3;
        $conn->query("update sub_results set total_score='$total_score',criteria_ctr1='$cp1',criteria_ctr2='$cp2',criteria_ctr3='$cp3', comments='$jcomment' where contestant_id='$contestant_id' AND judge_id='$judge_id'");
   }
   
   }
   else
   {
    $total_score=$cp1+$cp2+$cp3+$cp4;
     $conn->query("update sub_results set total_score='$total_score',criteria_ctr1='$cp1',criteria_ctr2='$cp2',criteria_ctr3='$cp3',criteria_ctr4='$cp4', comments='$jcomment' where contestant_id='$contestant_id' AND judge_id='$judge_id'");
   }
   }
   else
   {
    $total_score=$cp1+$cp2+$cp3+$cp4+$cp5;
       $conn->query("update sub_results set total_score='$total_score',criteria_ctr1='$cp1',criteria_ctr2='$cp2',criteria_ctr3='$cp3',criteria_ctr4='$cp4',criteria_ctr5='$cp5', comments='$jcomment' where contestant_id='$contestant_id' AND judge_id='$judge_id'");
   }
   
   }
   else
   {
    $total_score=$cp1+$cp2+$cp3+$cp4+$cp5+$cp6;
    $conn->query("update sub_results set total_score='$total_score',criteria_ctr1='$cp1',criteria_ctr2='$cp2',criteria_ctr3='$cp3',criteria_ctr4='$cp4',criteria_ctr5='$cp5',criteria_ctr6='$cp6', comments='$jcomment' where contestant_id='$contestant_id' AND judge_id='$judge_id'");
   }
   
   
    $conn->query("update contestants set status='finish' where contestant_id='$contestant_id'");
    
    
   ?>
    

<script>
window.location = 'judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=<?php echo $contestant_id; ?>&pStat=xChange';
alert('Score for <?php echo $contestant_name; ?> sent to Event Tabulators. Thank You!');						
</script>
 
 


 