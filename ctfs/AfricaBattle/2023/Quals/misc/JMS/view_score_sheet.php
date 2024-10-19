 
<!DOCTYPE html>
<html lang="en">
   
   <?php
   include('header2.php');
    include('session.php');
    error_reporting(0);
    $event_id=$_GET['event_id'];
    $judge_id=$_GET['judge_id'];
    ?>

  <body>

  <div class="container">

    <!-- Docs nav
    ================================================== -->
    <div class="row">
      
      <div class="span12">



        <!-- Download
        ================================================== -->
        
           <?php   
 

         
             $s_event_query = $conn->query("select * from sub_event where subevent_id='$event_id'") or die(mysql_error());
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
            <h2><?php echo $event_row['event_name']; ?></h2> 
             </td>
              </tr>
               <tr>
             <td align="center">
            <h3><?php echo $s_event_row['event_name']; ?></h3> 
             </td>
              </tr>
               
             </table>
             
             </center>
          
          <table class="table table-striped">
        <thead>
     <th>No. &amp; Contestant Name</th>
        <?php
        $criteria_query = $conn->query("select * from criteria where subevent_id='$event_id' ORDER BY criteria_ctr ASC") or die(mysql_error());
        while ($crit_row = $criteria_query->fetch()) {
        
         ?>
        <th><?php echo $crit_row['criteria']; ?></th>
        <?php } ?>
        <th>Total Score</th>
        <th>Rank</th>
        
        </thead>
     <tbody>
    
    <?php
    
  
        $score_query = $conn->query("select * from sub_results where subevent_id='$event_id' and judge_id='$judge_id' ORDER BY contestant_id ASC") or die(mysql_error());

	$num_rowxz = $score_query->rowcount();
    
if( $num_rowxz > 0 ) { 
while ($score_row = $score_query->fetch())
 {
 
     $s1=$score_row['criteria_ctr1'];
     $s2=$score_row['criteria_ctr2'];
     $s3=$score_row['criteria_ctr3'];
     $s4=$score_row['criteria_ctr4'];
     $s5=$score_row['criteria_ctr5'];
     $s6=$score_row['criteria_ctr6'];
     $s7=$score_row['criteria_ctr7'];
     $s8=$score_row['criteria_ctr8'];
     $s9=$score_row['criteria_ctr9'];
     $s10=$score_row['criteria_ctr10'];
     $total_score=$score_row['total_score']; 
     $rank=$score_row['rank'];
     $s_result_id=$score_row['subresult_id'];
     $con_id=$score_row['contestant_id'];
      
      
      
      ?>
         <tr>
        <td><?php
         $cont_query = $conn->query("select * from contestants where contestant_id='$con_id'") or die(mysql_error());
while ($cont_row = $cont_query->fetch())
{
    $c_num=$cont_row['contestant_ctr'];
  echo $c_num.". ".$cfnme=$cont_row['fullname'];   
}
        
         ?></td>
        
          <?php
          
        $criteria_query = $conn->query("select * from criteria where subevent_id='$event_id' ORDER BY criteria_ctr ASC") or die(mysql_error());
while ($crit_row = $criteria_query->fetch()) {
      
         ?>
        <td>
        
        <?php
 if($crit_row['criteria_ctr']==1)
 { ?>
     <?php echo $s1; ?> 
<?php } ?>


 <?php
 if($crit_row['criteria_ctr']==2)
 { ?>
     <?php echo $s2; ?> 
<?php } ?>


 <?php
 if($crit_row['criteria_ctr']==3)
 { ?>
    <?php echo $s3; ?> 
<?php } ?>


 <?php
 if($crit_row['criteria_ctr']==4)
 { ?>
    <?php echo $s4; ?> 
<?php } ?>


 <?php
 if($crit_row['criteria_ctr']==5)
 { ?>
    <?php echo $s5; ?> 
<?php } ?>


</td>



        <?php } ?>
        <td><?php echo $total_score; ?></td>
        <td><?php echo $rank;
 
        
        
         ?></td>
        
 
         </tr>
         
         
         
         
         
        <?php } ?>
        
    
     </tbody>
     
          </table>
          
          <?php $j_query = $conn->query("select * from judges where subevent_id='$event_id' and judge_id='$judge_id'") or die(mysql_error());
while ($j_row = $j_query->fetch()) { ?>
             <hr />
             <table align="right">
             <tr>
             <td align="center">
            <h4><?php echo $j_row['fullname']; ?></h4> 
            
             </td>
              </tr>
              <?php if($j_row['jtype']=="Chairman"){ ?>
                <tr>
             <td align="center">
            Chairman
             </td>
              </tr>
              <?php } ?>
         
               <tr>
             <td align="center">
            Event Judge
             </td>
              </tr>
               
             </table> <?php
     
 }
 }
 else
 {
    $s1="";
     $s2="";
     $s3="";
     $s4="";
     $s5="";
     $s6="";
     $s7="";
     $s8="";
     $s9="";
     $s10="";
      $total_score="";
 ?>
 
 <table align="center">
 <tr>
 <td>
 <div class="alert alert-warning">
 <h3>
 No data to Display... Judges not finish scoring at this moment.
 </h3>
 </div>
 </td>
 </tr>
 </table>
 
 <?php } ?>
       
            
           <?php }   } ?>
       
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
