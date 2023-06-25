 
<!DOCTYPE html>
<html lang="en">
   
   <?php
   include('header2.php');
   include('session.php');
   
   $active_sub_event=$_GET['event_id'];
 
 
 
 
            $c_ctr_query = $conn->query("select * from contestants where subevent_id='$active_sub_event'") or die(mysql_error());
            $c_ctr= $c_ctr_query->rowcount(); 
 
 
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
            <h4>Participant's Score Deductions</h4> 
             </td>
              </tr>
               
             </table>
             
             </center>
          
          <table class="table table-bordered">
        <thead>
        
     <th>Participant</th>
       
        <th>Score Summary</th>
      
          <th>Set Deduction</th>
        </thead>
     <tbody>
     
     
     <?php
        
$o_result_query = $conn->query("select distinct contestant_id from sub_results where subevent_id='$active_sub_event' ORDER BY contestant_id ASC") or die(mysql_error());
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
           <th>Judge</th>
           <th>Score</th>
           
            <th>Score with deduction</th>
       
           </tr>
         <?php

$divz=0;
 

$tot_score_query = $conn->query("select judge_id,total_score, deduction, rank from sub_results where contestant_id='$contestant_id' ORDER BY judge_id") or die(mysql_error());
while ($tot_score_row = $tot_score_query->fetch()) 
{
 
    ?>
    
  
   <tr>
   
   <td><?php $jx_id=$tot_score_row['judge_id'];
    $jname_query = $conn->query("select * from judges where judge_id='$jx_id'") or die(mysql_error());
    $jname_row = $jname_query->fetch();
    echo $jname_row['fullname'];
    ?></td>
    
   <td><?php echo $tot_score_row['total_score']; ?></td>
   
   <td><?php echo $tot_score_row['total_score']-$tot_score_row['deduction']; ?><?php echo " (-".$tot_score_row['deduction'].")"; ?></td>
     
   </tr>
  
 
  
<?php } ?>
 

 </table>
          </td>
          
          <td>
          <form method="POST">
          <input type="hidden" name="active_main_event" value="<?php echo $MEidxx; ?>"  />
          <input type="hidden" name="active_sub_event" value="<?php echo $active_sub_event; ?>"  />
          <input type="hidden" name="contestant_id" value="<?php echo $contestant_id; ?>"  />
          <select name="deduction" style="width: 100% !important;"> 
          
          <option>0</option>
          <option>1</option>
          <option>2</option>
          <option>3</option>
          <option>4</option>
          <option>5</option>
          <option>6</option>
          <option>7</option>
          <option>8</option>
          <option>9</option>
          <option>10</option>
          
          
          
          </select><br />
      
             <button name="submit_place" class="btn btn-danger pull-right"><i class="icon-ok"></i> <strong>SUBMIT</strong></button>
       
            
     
          </form>
          </td>
         </tr>
         
         
 
         
         
        <?php } ?>
        
    
     </tbody>
     
          </table>
          
            
           <?php } } ?>
     
    </div>

  </div>
  
  </div>
 <?php 
 if(isset($_POST['submit_place']))
 {
    $MEidxx=$_POST['active_main_event'];
    $active_sub_event=$_POST['active_sub_event'];
    $contestant_id=$_POST['contestant_id'];
    $deduction=$_POST['deduction'];
    
    $conn->query("update sub_results set deduction='$deduction' where subevent_id='$active_sub_event' and contestant_id='$contestant_id'");
   ?>
 <script>
window.location = 'deductScores.php?event_id=<?php echo $active_sub_event; ?>';
alert('Participant scores deducted...');						
</script>        
 <?php }
 ?>

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
