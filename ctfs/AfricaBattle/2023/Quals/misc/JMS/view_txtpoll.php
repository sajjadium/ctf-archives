   
     <script type="text/javascript">
var auto_refresh = setInterval(
function ()
{
$('#load_tweets3').load('ref_view_txtpoll.php');
}, 3000); //refresh div every 10000 milliseconds or 10 seconds
</script>




 <div id="load_tweets3"> 
 <?php   error_reporting(0);
 
  ?>
  
  
   
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="css/bootstrap.css" media="screen"/>
    <link rel="stylesheet" href="css/custom.min.css"/>
    <link rel="stylesheet" href="css/font-awesome.css" media="screen"/>
    <link rel="stylesheet" href="css/font-awesome.min.css"/>
</head>
   
   <?php
   include('header2.php');
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
             <table>
             <tr>
             <td align="center">
            <h2><?php echo $event_row['event_name']; ?></h2> 
             </td>
              </tr>
               <tr>
             <td align="center">
            <h3>Textpoll Live View - <?php echo $s_event_row['event_name']; ?></h3> 
             </td>
              </tr>
               
             </table>
             
             </center>
          
 

 

 
<?php 
 

$tp_query = $conn->query("select DISTINCT Id from messagein where sendStatus=''") or die(mysql_error());

while ($tp_row = $tp_query->fetch()) 
{
    
    
     
      $IdXz=$tp_row['Id'];
     
        
      $tpx_query = $conn->query("select * from messagein WHERE Id='$IdXz'") or die(mysql_error());
      $tpx_row = $tpx_query->fetch();
      
      
     $frommmm=$tpx_row['MessageFrom'];
  
     $txtMessage=$tpx_row['MessageText'];
 
     $sendTo="+".$frommmm;
                
        
        
        $cname_query = $conn->query("select * from contestants where txt_code='$txtMessage'") or die(mysql_error());
        
        
        
        if($cname_query->rowcount()>0 )
        {

       $txtCoderow = $cname_query->fetch();
            
 
            
  $txtcode=$txtCoderow['txt_code'];
    
      $txtPollScore=$txtCoderow['txtPollScore'];
            
                    $tpxxxx_query = $conn->query("select distinct MessageText from messagein where MessageFrom='$frommmm' AND sendStatus='read'") or die(mysql_error());

                    
                    if($tpxxxx_query->rowCount()>0)
                    {               
                
      $MessageText="You have voted previously. Your vote is not counted.";
                                
                                $conn->query("insert into messageout(MessageTo,MessageFrom,MessageText)values('$sendTo','BCC EJS','$MessageText')");
                                
                                 $updateSS_query = $conn->query("UPDATE messagein SET sendStatus='readX' where Id='$IdXz'") or die(mysql_error());
        
                    
                    }
                    else
                    {
                        
                     
           
      $txtPollScore=$txtPollScore+1; 
             
      $MessageText="Thank you. Your vote has been counted.";
                      
                      $conn->query("insert into messageout(MessageTo,MessageFrom,MessageText)values('$sendTo','BCC EJS','$MessageText')");  
        
                    $updateScore_query = $conn->query("UPDATE contestants SET txtPollScore='$txtPollScore' where txt_code='$txtMessage'") or die(mysql_error());
                    
                    $updateSS_query = $conn->query("UPDATE messagein SET sendStatus='read' where Id='$IdXz'") or die(mysql_error());
        
                    
                    }
               
        }
        else
        {
                       
              
     $MessageText="Wrong code. Pls. try again.";
                      
                      $conn->query("insert into messageout(MessageTo,MessageFrom,MessageText)values('$sendTo','BCC EJS','$MessageText')");  
                        
                        $updateSS_query = $conn->query("UPDATE messagein SET sendStatus='readX' where Id='$IdXz'") or die(mysql_error());
        
        }
        


                
               
} ?>
  <table width="800" align="center">
<?php 

$totAllScore=0;

$showContTP_queryxxxx = $conn->query("select * from contestants WHERE subevent_id='$active_sub_event'") or die(mysql_error());
      while($showContTProwxxx=$showContTP_queryxxxx->fetch())   
      {
      
         $totAllScore=$totAllScore+$showContTProwxxx['txtPollScore']; 
        }
        
$showContTP_query = $conn->query("select * from contestants WHERE subevent_id='$active_sub_event'") or die(mysql_error());
      while($showContTProw=$showContTP_query->fetch())   
      {
        
     
         $barPercent=($showContTProw['txtPollScore']/$totAllScore)*100;
         
        ?>
        
        <tr>
        
        
        <td>
       
            <h3 id="progress-animated"><?php  echo $showContTProw['fullname']; ?></h3>
            <div class="bs-component">
              <div class="progress progress-striped active">
                <div class="progress-bar" style="width: <?php echo $barPercent; ?>%"></div>
              </div>
            </div>
        
        
      
             
        
        </td >
        
      <td> &nbsp;</td>
       <td width="50">
        <h1><?php  echo $barPercent; ?>%</h1></td>
        
        
            
            
            
            
        
            
        
        
        
        
        
      <?php } ?>
       </table>
        <?php }  }  ?>
       
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
    
    
    
    <script src="javascript/jquery1102.min.js"></script>
    <script src="javascript/bootstrap.min.js"></script>
    <script src="javascript/custom.js"></script>
 

  </body>
</html>


  
  
 </div>