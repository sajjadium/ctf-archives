<link rel="shortcut icon" href="bcc_logo.png"/>
    
<script type="text/javascript">
var auto_refresh = setInterval(
function ()
{
$('#load_tweets2').load('ref_view.php');
}, 5000); //refresh div every 10000 milliseconds or 10 seconds
</script>




 <div id="load_tweets2"> 
 <?php  
 
 
include('ref_view.php');
 
  ?>
 
 </div>