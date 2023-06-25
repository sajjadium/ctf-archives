 
<!DOCTYPE html>
<html lang="en">
   
   <?php
   include('header2.php');
    include('session.php');
  
  
  
    $active_main_event=$_GET['mainevent_id'];
   $active_sub_event=$_GET['sub_event_id'];
    ?>
<style style="text/css">
@media print {
    footer {page-break-after: always;}
}
</style>
  <body data-spy="scroll" data-target=".bs-docs-sidebar">
 
 


  <div class="container">

    <!-- Docs nav
    ================================================== -->
    <div class="row">
      
      <div class="span12">



        <!-- Download
        ================================================== -->
        
           <?php   
          $event_query = $conn->query("select * from main_event where mainevent_id='$active_main_event'") or die(mysql_error());
		while ($event_row = $event_query->fetch()) 
        { 
             $s_event_query = $conn->query("select * from sub_event where subevent_id='$active_sub_event'") or die(mysql_error());
		while ($s_event_row = $s_event_query->fetch()) 
        {
            
            ?>
        
             <center>
             
             <?php include('doc_header.php'); ?>
             
             
             <table>
             <tr>
             <td align="center">
            <h2><?php echo $event_row['event_name']; ?></h2> 
             </td>
              </tr>
               <tr>
             <td align="center">
            <h3>Over All Result - <?php echo $s_event_row['event_name']; ?></h3> 
             </td>
              </tr>
               
             </table>
             
             </center>
          
          <table class="table table-bordered">
        <thead>
        
     <th>No. & Contestant Name</th>
       
        
        <th>Result Summary</th>
         <th>Place Title</th>
        </thead>
     <tbody>
     
     
     <?php
        $o_result_query = $conn->query("select distinct contestant_id from sub_results where mainevent_id='$active_main_event' and subevent_id='$active_sub_event' order by place_title ASC") or die(mysql_error());
while ($o_result_row = $o_result_query->fetch()) {
    
    $contestant_id=$o_result_row['contestant_id'];
    
    
         ?>
         <tr>
         <td><?php
          $cname_query = $conn->query("select * from contestants where contestant_id='$contestant_id'") or die(mysql_error());
while ($cname_row = $cname_query->fetch()) 
{
    
        echo $cname_row['contestant_ctr'].".".$cname_row['fullname']; 
    
}
           ?></td>
          <td>
          
 <table class="table table-bordered">
           <tr>
         
           <th>Average Score</th>
           <th>Sum of Rank in all Judges</th>
           </tr>
         <?php

$divz=0;
$c_ctr=0;
$totx_score=0;
$rank_score=0;
$tot_score_query = $conn->query("select * from sub_results where contestant_id='$contestant_id'") or die(mysql_error());
while ($tot_score_row = $tot_score_query->fetch()) 
{
  $divz=$divz+1;  
   $c_ctr=$c_ctr+1;
   $place_title=$tot_score_row['place_title'];
} 


$tot_score_query = $conn->query("select judge_id,total_score,rank from sub_results where contestant_id='$contestant_id'") or die(mysql_error());
while ($tot_score_row = $tot_score_query->fetch()) 
{
     $totx_score=$totx_score+$tot_score_row['total_score'];
     $rank_score=$rank_score+$tot_score_row['rank'];
    ?>
    
  
    <?php  $tot_score_row['judge_id']; ?> 
   <?php  $tot_score_row['total_score']; ?> 
   <?php  $tot_score_row['rank']; ?> 
    
  
 
  
<?php } ?>
 

 <tr>
 
   <td><b>Ave: <?php echo round($totx_score/$divz,2) ?></b></td>
      <td><b>Sum: <?php  echo $rank_score; ?></b></td>
   </tr>

 </table>

          </td>
          <td><center><h3><?php echo $place_title; ?></h3></center></td>
         </tr>
         
         
 
         
         
        <?php } ?>
        
    
     </tbody>
     
          </table>
          
            <hr />
            <br />
             <table align="center">  
              <tr>
            <?php
            $jjn_result_query = $conn->query("select distinct judge_id from sub_results where mainevent_id='$active_main_event' and subevent_id='$active_sub_event' order by judge_id ASC") or die(mysql_error());
while ($jjn_result_row = $jjn_result_query->fetch()) {
      $jx_id=$jjn_result_row['judge_id'];
      
    $jname_query = $conn->query("select * from judges where judge_id='$jx_id'") or die(mysql_error());
$jname_row = $jname_query->fetch();

    ?>
            <td>
            <table>
            <tr><td align="center">&nbsp;&nbsp;&nbsp;<u><strong><?php echo $jname_row['fullname'];?></strong></u>&nbsp;&nbsp;&nbsp;</td></tr>
             <tr><td align="center">Judge</td></tr>
            </table>
            </td>
    
           
  
<?php }?>
</tr>
</tr>
   </table> 
<hr />
     <table align="center">  
              <tr>
           
            <?php
            $jjn_result_query = $conn->query("select * from organizer where org_id='$session_id'") or die(mysql_error());
while ($jjn_result_row = $jjn_result_query->fetch()) {
      

    ?>
            <td>
            <table>
            <tr><td align="center">&nbsp;&nbsp;&nbsp;<u><strong><?php echo $jjn_result_row['fname']." ".$jjn_result_row['mname']." ".$jjn_result_row['lname'];?></strong></u>&nbsp;&nbsp;&nbsp;</td></tr>
             <tr><td align="center">Tabulator</td></tr>
            </table>
            </td>
    
           
  
<?php }?>
</tr>
</table>
<hr />
 <table align="center"> 
 
              <tr>
          <?php
            $jjn_result_query = $conn->query("select * from organizer where organizer_id='$session_id'") or die(mysql_error());
while ($jjn_result_row = $jjn_result_query->fetch()) {
      

    ?>
            <td>
            <table>
            <tr><td align="center">&nbsp;&nbsp;&nbsp;<u><strong><?php echo $jjn_result_row['fname']." ".$jjn_result_row['mname']." ".$jjn_result_row['lname'];?></strong></u>&nbsp;&nbsp;&nbsp;</td></tr>
             <tr><td align="center">Organizer</td></tr>
            </table>
            </td>
    
           
  
<?php }?>
</tr>
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


    <!-- Analytics
    ================================================== -->
    <script>
      var _gauges = _gauges || [];
      (function() {
        var t   = document.createElement('script');
        t.type  = 'text/javascript';
        t.async = true;
        t.id    = 'gauges-tracker';
        t.setAttribute('data-site-id', '4f0dc9fef5a1f55508000013');
        t.src = '//secure.gaug.es/track.js';
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(t, s);
      })();
    </script>

  </body>
</html>
