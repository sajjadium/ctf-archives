 
<!DOCTYPE html>
<html lang="en">
   
   <?php
   error_reporting(0);
   
   include('header2.php');
   include('session.php');
   
   $active_sub_event=$_GET['event_id'];
 
  function ordinal($i)
  {
      $l = substr($i,-1);
      $s = substr($i,-2,-1);
      
      return $i.(
        (($l==1 && $s==1) ||
        ($l==2 && $s==1) ||
        ($l==3 && $s==1) || 
        $l > 3 ||
        $l==0 )?'th':(($l==3)?'rd':(($l==2)?'nd':'st')));
  }     
$s_event_query = $conn->query("select * from sub_event where subevent_id='$active_sub_event'") or die(mysql_error());
while ($s_event_row = $s_event_query->fetch()) 
{
            
            $MEidxx=$s_event_row['mainevent_id'];
            
              $event_query = $conn->query("select * from main_event where mainevent_id='$MEidxx'") or die(mysql_error());
		while ($event_row = $event_query->fetch()) 
        {
            
         
        
            $o_result_query = $conn->query("select distinct contestant_id from sub_results where mainevent_id='$MEidxx' and subevent_id='$active_sub_event'") or die(mysql_error());
            while ($o_result_row = $o_result_query->fetch())
            {
            
            $contestant_id=$o_result_row['contestant_id'];
             
            
         
                $rank_score=0;
         
         
                $tot_score_query = $conn->query("select judge_id,total_score, deduction, rank from sub_results where contestant_id='$contestant_id'") or die(mysql_error());
                while ($tot_score_row = $tot_score_query->fetch()) 
                {
                    
                     $rank_score=$rank_score+$tot_score_row['rank'];
                       
                }
              
               
               
                $rank_score; 
                
                $rsChecker = $conn->query("select * from rank_system WHERE subevent_id='$active_sub_event' AND contestant_id='$contestant_id'") or die(mysql_error());
                
                if($rsChecker->rowCount()>0)
                {
                    $conn->query("UPDATE rank_system SET total_rank='$rank_score' WHERE subevent_id='$active_sub_event' AND contestant_id='$contestant_id'"); 
                }
                else
                {
                    $conn->query("insert into rank_system(subevent_id,contestant_id,total_rank)VALUES('$active_sub_event','$contestant_id','$rank_score')"); 
                }
        
         
    
       
          
                  $rspCtr=0;
                  $rsPlacer = $conn->query("SELECT * FROM rank_system WHERE subevent_id='$active_sub_event' ORDER BY total_rank ASC") or die(mysql_error());
                  while ($rsp_row = $rsPlacer->fetch()) 
                  {
                    $rspCtr++;
                    
                    $rsp_contestant_id=$rsp_row['contestant_id'];
                    $conn->query("UPDATE sub_results SET place_title='".(ordinal($rspCtr))."' WHERE contestant_id='$rsp_contestant_id'");
                    // if($rspCtr==1)
                    // {
                    //     $conn->query("UPDATE sub_results SET place_title='1st' WHERE contestant_id='$rsp_contestant_id'"); 
                    // }
                    
                    
                    // if($rspCtr==2)
                    // {
                    //     $conn->query("UPDATE sub_results SET place_title='2nd' WHERE contestant_id='$rsp_contestant_id'"); 
                    // }
                    
                    
                    // if($rspCtr==3)
                    // {
                    //     $conn->query("UPDATE sub_results SET place_title='3rd' WHERE contestant_id='$rsp_contestant_id'"); 
                    // }
                    
                    
                    // if($rspCtr==4)
                    // {
                    //     $conn->query("UPDATE sub_results SET place_title='4th' WHERE contestant_id='$rsp_contestant_id'"); 
                    // }
                    
                  }

        } 
    }  
           
} 
?>

 
 
 

  <body data-spy="scroll" data-target=".bs-docs-sidebar">
 
 


  <div class="container">

    <!-- Docs nav
    ================================================== -->
    <div class="row">
      
      <div class="span12">



        <!-- Download
        ================================================== -->
        
           <?php   
           
             $s_event_query = $conn->query("select * from sub_event where subevent_id='$active_sub_event'") or die(mysql_error());
		while ($s_event_row = $s_event_query->fetch()) 
        {
            
            $MEidxx=$s_event_row['mainevent_id'];
            
              $event_query = $conn->query("select * from main_event where mainevent_id='$MEidxx'") or die(mysql_error());
		while ($event_row = $event_query->fetch()) 
        {
            
            ?>
        
             <center>
             
   
                <?php include('doc_header.php'); ?>
                
   
      
             <table>
             <tr>
             <td align="center">
            <h3><?php echo $event_row['event_name']; ?></h3> 
             </td>
              </tr>
              <tr>
              <td align="center">
              <h4> <?php echo $s_event_row['event_name']; ?></h4>
              </td>
              </tr>
               <tr>
             <td align="center">
            <h4>Participant's Placing Results</h4> 
             </td>
              </tr>
               
             </table>
             
             </center>
          
          <table class="table table-bordered">
        <thead>
        
     <th>Participant</th>
       
        
        <th>Summary of Scores</th>
          <th>Participant's Placing</th>
        </thead>
     <tbody>
     
     
     <?php
        
$o_result_query = $conn->query("select distinct contestant_id from sub_results where mainevent_id='$MEidxx' and subevent_id='$active_sub_event' ORDER BY contestant_id ASC") or die(mysql_error());
while ($o_result_row = $o_result_query->fetch()) {
    
    $contestant_id=$o_result_row['contestant_id'];
     
    
    
         ?>
         <tr>
         <td><h5><?php
   
          $cname_query = $conn->query("select * from contestants where contestant_id='$contestant_id'") or die(mysql_error());
while ($cname_row = $cname_query->fetch()) 
{
  
        $contXXname=$cname_row['contestant_ctr'].".".$cname_row['fullname']; 
    
}
            echo $contXXname;  ?>
           
           </h5></td>
           
           
          <td>
           <table class="table table-bordered">
           <tr>
           <th>Judge</th>
           <th>Score</th>
           <th>Rank</th>
           </tr>
         <?php

$divz=0;
$totx_score=0;
$rank_score=0;
 
$tot_score_query = $conn->query("select * from sub_results where contestant_id='$contestant_id'") or die(mysql_error());
while ($tot_score_row = $tot_score_query->fetch()) 
{
  $divz=$divz+1;  

   $place_title=$tot_score_row['place_title'];
  
} 


$tot_score_query = $conn->query("select judge_id,total_score, deduction, rank from sub_results where contestant_id='$contestant_id' ORDER BY judge_id") or die(mysql_error());
while ($tot_score_row = $tot_score_query->fetch()) 
{
     $totx_score=$totx_score+$tot_score_row['total_score'];
     $rank_score=$rank_score+$tot_score_row['rank'];
     $totx_deduct=$tot_score_row['deduction'];
     
    ?>
    
  
   <tr>
   <td style="width: 50% !important;"><?php $jx_id=$tot_score_row['judge_id'];
    $jname_query = $conn->query("select * from judges where judge_id='$jx_id'") or die(mysql_error());
$jname_row = $jname_query->fetch();
 echo $jname_row['fullname'];
    ?></td>
   <td style="width: 25% !important;"><?php echo $tot_score_row['total_score']-$tot_score_row['deduction']; ?><?php echo " (-".$tot_score_row['deduction'].")"; ?></td>
    <td style="width: 25% !important;"><?php echo $tot_score_row['rank']; ?></td>
   </tr>
  
 
  
<?php } ?>
 

 <tr>
 <td></td>
   <td><b>Ave: <?php echo round(($totx_score-$totx_deduct)/$divz,2) ?></b></td>
      <td><b>Sum:
      <?php
      
      
        echo $rank_score; 


        ?></b></td>
   </tr>

 </table>
          </td>
          
 
          
          <td style="width: 17%!important;">
          <center>
          <h3>
          <?php
          
          $pt_result_query = $conn->query("SELECT * FROM sub_results WHERE contestant_id='$contestant_id'") or die(mysql_error());
          $pt_result_row = $pt_result_query->fetch();
    
          echo $pt_result_row['place_title'];
          
          
          ?>
          </h3>
          <hr />
          <?php echo $contXXname; ?>
          </center>
          </td>
          
          
          
          
          
          
         </tr>
         
         
 
         
         
        <?php } ?>
        
    
     </tbody>
     
          </table>
          
            
           <?php }  } ?>
     
    </div>

  </div>
 
 
</div>


<?php include('footer.php'); ?>

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>
    <script src="assets/js/jquery.js"></script>
    <script src="assets/js/bootstrap-transition.js"></script>
    <script src="assets/js/bootstrap-alert.js"></script>
    <script src="assets/js/bootstrap-modal.js"></script>
    <script src="assets/js/bootstrap-dropdown.js"></script>
    <script src="assets/js/bootstrap-scrollspy.js"></script>
    <script src="assets/js/bootstrap-tab.js"></script>
    <script src="assets/js/bootstrap-tooltip.js"></script>
    <script src="assets/js/bootstrap-popover.js"></script>
    <script src="assets/js/bootstrap-button.js"></script>
    <script src="assets/js/bootstrap-collapse.js"></script>
    <script src="assets/js/bootstrap-carousel.js"></script>
    <script src="assets/js/bootstrap-typeahead.js"></script>
    <script src="assets/js/bootstrap-affix.js"></script>

    <script src="assets/js/holder/holder.js"></script>
    <script src="assets/js/google-code-prettify/prettify.js"></script>

    <script src="assets/js/application.js"></script>


  </body>
</html>
