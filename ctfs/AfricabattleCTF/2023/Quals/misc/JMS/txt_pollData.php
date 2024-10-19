 
<!DOCTYPE html>
<html lang="en">
   
   <?php
   include('header.php');
    include('session.php');
    $active_sub_event=$_GET['sid'];
  error_reporting(0);
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
            $active_main_event=$s_event_row['mainevent_id'];
            
             $event_query = $conn->query("select * from main_event where mainevent_id='$active_main_event'") or die(mysql_error());
		while ($event_row = $event_query->fetch()) 
        { 
            
            ?>
            
             <center>
             
             <?php include('doc_header.php'); ?>
  
            <h3><?php echo $event_row['event_name']; ?></h3> 
        
            <h4>Textpoll Live View</h4> 
 
         
     
     <?php
        $o_result_query = $conn->query("select * from contestants where subevent_id='$active_sub_event' order by contestant_id ASC") or die(mysql_error());
while ($o_result_row = $o_result_query->fetch()) {
    
    $contestant_id=$o_result_row['contestant_id']; 
    
    ?>
 
 
 
    <div class="col-lg-12">
 <div class="panel panel-primary">
          
            
<?php         
$cname_query = $conn->query("select * from contestants where contestant_id='$contestant_id'") or die(mysql_error());
while ($cname_row = $cname_query->fetch()) 
{ 
    $txtcode=$cname_row['txt_code'];
    
    ?>
 
 <?php 
 
 $txtpoll_score=0;
  $tpx_query = $conn->query("select distinct MessageFrom from messagein") or die(mysql_error());
while ($tpx_row = $tpx_query->fetch()) 
{
    $frommmm=$tpx_row['MessageFrom'];

 $tp_query = $conn->query("select distinct MessageText from messagein where MessageFrom='$frommmm'") or die(mysql_error());
while ($tp_row = $tp_query->fetch()) 
{
    $txtMessage=$tp_row['MessageText'];
    if($txtcode==$txtMessage)
    {
    $txtpoll_score=$txtpoll_score+1;    
    }
  
} } ?>

<div class="panel-heading">
<h3 class="panel-title"><?php echo $s_event_row['event_name']; ?> Textpoll - Vote for #<strong><?php echo $cname_row['contestant_ctr']; ?> <?php echo $cname_row['fullname']; ?></strong></h3>
</div>

     <div class="panel-body">
  
           <font size="5">TEXT <strong style="color: blue;"><?php  echo $txtcode; ?></strong> AND SEND TO <i style="color: blue;"><?php echo $txt_poll_num; ?></i></font> 
 
</div>

 
 
 <?php }
 $txtpoll_score=0;
  ?> 
 
          </div>
          
        
  </div>
         
        <?php } }  } ?>
       
    </div>

  </div>
 
 <a href="#" title="Back to Top" class="btn btn-default pull-right"><i class="glyphicon glyphicon-chevron-up"></i></a>

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
