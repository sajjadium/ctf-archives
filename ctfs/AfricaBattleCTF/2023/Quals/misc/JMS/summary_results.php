<!DOCTYPE html>
<html lang="en">
   
   <?php
   
include('header.php');
include('session.php');

$active_main_event=$_GET['main_event_id'];
 
    ?>
 
 
 
 <body>

 
 <div class="container">

 
      <div class="span12">

        
           <?php   
          $event_query = $conn->query("select * from main_event where mainevent_id='$active_main_event'") or die(mysql_error());
		while ($event_row = $event_query->fetch()) 
        { 
 
            ?>
        
             <center>
             
             <?php include('doc_header.php'); ?>
             
             
             <table>
        <tr>
             <td align="center">
            <h3><strong><?php echo $event_row['event_name']; ?></strong></h3> 
             </td>
              </tr>
               <tr>
                <td align="center">
                <h3>Tally Sheet</h3>
                </td>
              </tr>
               
             </table>
             
             </center>
              <?php }  ?>
        <section id="download-bootstrap">
          <div class="page-header">
 
<table style="width: 100% !important;" align="center">
  
                            
                           
                            
                        
            
<?php   
$sy_query = $conn->query("select DISTINCT sy FROM main_event where organizer_id='$session_id' AND mainevent_id='$active_main_event='") or die(mysql_error());
while ($sy_row = $sy_query->fetch()) 
{
            
$sy=$sy_row['sy'];
 
$MEctrQuery = $conn->query("select * FROM main_event where sy='$sy'") or die(mysql_error());
$MECtr = $MEctrQuery->rowCount();  ?>

    
 
<tr>

<td>   
       
                        <?php   
                        $event_query = $conn->query("select * from main_event where organizer_id='$session_id' AND sy='$sy'") or die(mysql_error());
                        while ($event_row = $event_query->fetch()) 
                        {
                            
                        $main_event_id=$event_row['mainevent_id'];
                        
                        
                        $SEctrQuery = $conn->query("select * FROM sub_event where mainevent_id='$main_event_id'") or die(mysql_error());
                        while($SECtr = $SEctrQuery->fetch())
                        {
                            $rs_subevent_id=$SECtr['subevent_id'];
                        
                        
                         ?>
                                    
                                    
                                    <h4>EVENT: <strong><?php echo $SECtr['event_name']; ?></strong></h4>
                                    <hr />
                                    
                                    <table align="center" class="table table-bordered" id="example">
                                    
                                     
                                    
                                    <?php   
                                    $contxx_query = $conn->query("select DISTINCT fullname from contestants where subevent_id='$rs_subevent_id'") or die(mysql_error());
                                    while ($contxx_row = $contxx_query->fetch()) 
                                    { ?>
                                    
                                    <th><strong><center><?php echo $contxx_row['fullname']; ?></center></strong></th>
                                    
                                    <?php } ?> 
                        
                                    
                            
                                    
                                         
                                    <tr>
                           
                                    <?php  
                                  
                                    $contxxz_query = $conn->query("select contestant_id from contestants where subevent_id='$rs_subevent_id'") or die(mysql_error());
                                    while ($contxxz_row = $contxxz_query->fetch()) 
                                    {  
                                    
                                    $contxzID=$contxxz_row['contestant_id'];
                                    
                                    $place_query = $conn->query("select DISTINCT place_title from sub_results where contestant_id='$contxzID' AND subevent_id='$rs_subevent_id'") or die(mysql_error());
                                    while ($place_row = $place_query->fetch()) 
                                    { ?>
                                    
                                    <td><strong><center><?php echo $place_row['place_title']; ?></center></strong></td>
                                    
                                    <?php   }   }   ?>
                                    
                                    </tr>
                             
                                    
                                    </table>
            
                                     
                                    <!-- End of List of sub-events -->
             
                        
                        <?php  }} ?>
      
                     
                                 
                       
 </td>
 </tr>
 
 
  <?php  }  ?>
 
  </table>
  </div>
 
 
  </section>

 
      </div>
    </div>

  <?php include('footer.php'); ?>


    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
 
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
 