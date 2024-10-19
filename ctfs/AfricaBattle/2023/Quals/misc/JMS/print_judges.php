 
 
   
<!DOCTYPE html>
<html lang="en">
   
   <?php
   include('header2.php');
   include('session.php');
    
    
    $sub_event_id=$_GET['sub_event_id'];
    $se_name=$_GET['se_name'];
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
       
            
        
             $s_event_query = $conn->query("select * from sub_event where subevent_id='$sub_event_id'") or die(mysql_error());
		while ($s_event_row = $s_event_query->fetch()) 
        {
            
            $active_main_event=$s_event_row['mainevent_id'];
            
            $event_query = $conn->query("select * from main_event where mainevent_id='$active_main_event'") or die(mysql_error());
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
            <h3>Judge Code for <?php echo $se_name; ?></h3> 
             </td>
              </tr>
               
             </table>
             
             </center>
 
 
                 <table class="table table-bordered">
  <thead>
 
   <th>No.</th>
  <th>Fullname</th>
  <th>Code</th>
   
  
  </thead>
   
  <tbody>
  <?php    
   	$judge_query = $conn->query("SELECT * FROM judges WHERE subevent_id='$sub_event_id' order by judge_ctr") or die(mysql_error());
    while ($judge_row = $judge_query->fetch()) 
        { ?>
  <tr>
  
     <td><?php echo $judge_row['judge_ctr']; ?></td>
    <td><?php echo $judge_row['fullname']; ?></td>
     <td><h2><?php echo $judge_row['code']; ?></h2></td>
    
        
  </tr>
 

   


   <?php } ?>
  </tbody>
 </table>    
  <div class="pull-right"><strong>Press Ctrl+P to Print</strong></div>
  
  
  
           <?php } } ?>
       
    </div>

  </div>
 
 <?php include('footer.php'); ?>
 
 </div>
 


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
