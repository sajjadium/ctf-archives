<?php 
 
  error_reporting(0);
    include('header2.php');
    include('session.php');
 
 
   $contestant_name=$_POST['contestant_name'];
   $contestant_id=$_POST['contestant_id'];
  $judge_id=$_POST['judge_id'];
   $judge_ctr=$_POST['judge_ctr'];
   $mainevent_id=$_POST['mainevent_id'];   
  $subevent_id=$_POST['subevent_id'];
  $jcomment=$_POST['jcomment'];   
  
  
   $conn->query("update sub_results set judge_rank_stat='' where subevent_id='$subevent_id' AND judge_id='$judge_id'");
   
   
   $cp15=$_POST['cp15'];
   $cp14=$_POST['cp14'];
   $cp13=$_POST['cp13'];
   $cp12=$_POST['cp12'];
   $cp11=$_POST['cp11'];
   $cp10=$_POST['cp10'];
   $cp9=$_POST['cp9'];
   $cp8=$_POST['cp8'];
   $cp7=$_POST['cp7'];
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
    
    /* criteria1-2 points */
    {
     $total_score=$cp1+$cp2;
    $conn->query("insert into sub_results(mainevent_id,subevent_id,contestant_id,judge_id,total_score,criteria_ctr1,criteria_ctr2,comments)
   values('$mainevent_id','$subevent_id','$contestant_id','$judge_id','$total_score','$cp1','$cp2','$jcomment')");   
    }
    
    
   }
   else
   
   
   /* criteria1-3 points */
   {
    $total_score=$cp1+$cp2+$cp3;
    $conn->query("insert into sub_results(mainevent_id,subevent_id,contestant_id,judge_id,total_score,criteria_ctr1,criteria_ctr2,criteria_ctr3,comments)
   values('$mainevent_id','$subevent_id','$contestant_id','$judge_id','$total_score','$cp1','$cp2','$cp3','$jcomment')");
   }
   
   
   /* criteria1-4 points */
   }
   else
   {
    $total_score=$cp1+$cp2+$cp3+$cp4;
    $conn->query("insert into sub_results(mainevent_id,subevent_id,contestant_id,judge_id,total_score,criteria_ctr1,criteria_ctr2,criteria_ctr3,criteria_ctr4,comments)
   values('$mainevent_id','$subevent_id','$contestant_id','$judge_id','$total_score','$cp1','$cp2','$cp3','$cp4','$jcomment')");
   }
   
   
   
   /* criteria1-5 points */
   }
   else
   {
    $total_score=$cp1+$cp2+$cp3+$cp4+$cp5;
    $conn->query("insert into sub_results(mainevent_id,subevent_id,contestant_id,judge_id,total_score,criteria_ctr1,criteria_ctr2,criteria_ctr3,criteria_ctr4,criteria_ctr5,comments)
   values('$mainevent_id','$subevent_id','$contestant_id','$judge_id','$total_score','$cp1','$cp2','$cp3','$cp4','$cp5','$jcomment')");
   }
   
   }
   
   /* criteria1-6 points */
   else
   {
    $total_score=$cp1+$cp2+$cp3+$cp4+$cp5+$cp6;
    $conn->query("insert into sub_results(mainevent_id,subevent_id,contestant_id,judge_id,total_score,criteria_ctr1,criteria_ctr2,criteria_ctr3,criteria_ctr4,criteria_ctr5,criteria_ctr6,comments)
   values('$mainevent_id','$subevent_id','$contestant_id','$judge_id','$total_score','$cp1','$cp2','$cp3','$cp4','$cp5','$cp6','$jcomment')");
   }
   
   
    $conn->query("update contestants set status='finish' where contestant_id='$contestant_id'");
    
    
   ?>
    
<script>
window.location = 'judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=<?php echo $contestant_id; ?>';
alert('Score for <?php echo $contestant_name; ?> sent to Event Tabulators. Thank You!');						
</script>

 
 


 