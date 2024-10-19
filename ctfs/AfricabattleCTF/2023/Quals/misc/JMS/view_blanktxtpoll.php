   
     <script type="text/javascript">
var auto_refresh = setInterval(
function ()
{
$('#load_tweets3').load('ref_view_blanktxtpoll.php');
}, 3000); //refresh div every 10000 milliseconds or 10 seconds
</script>




 <div id="load_tweets3"> 
 <?php   error_reporting(0);
 // Turn off error reporting
  include('ref_view_blanktxtpoll.php'); 
  ?>
 </div>
 
 
  