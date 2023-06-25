 

<!DOCTYPE html>
<html lang="en">
  
  <?php 
  include('header.php');
    include('session.php');
    
    
    $sub_event_id=$_GET['sub_event_id'];
    $se_name=$_GET['se_name'];
    $contestant_id=$_GET['contestant_id'];
     
  ?>
  
  <body>
    <!-- Navbar
    ================================================== -->
    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
       
            
        </div>
      </div>
    </div>
<header class="jumbotron subhead" id="overview">
  <div class="container">
    <h1><?php echo $se_name; ?> Settings</h1>
    <p class="lead">Judging System</p>
  </div>
</header>


<div class="container">

<div class="span12">



                <br />
                <div class="col-md-12">
                    <ul class="breadcrumb">
                    
                        <li><a href="selection.php">User Selection</a></li>
                    
                        <li><a href="home.php">List of Events</a></li>
                        
                        <li><a href="sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id; ?>&se_name=<?php echo $se_name; ?>"><?php echo $se_name; ?> Settings</a></li>
                        
                        <li>Set Text Code</li>
                        
                    </ul>
                </div>
                

   <form method="POST">
    <input value="<?php echo $sub_event_id; ?>" name="sub_event_id" type="hidden" />
 <input value="<?php echo $se_name; ?>" name="se_name" type="hidden" />
 <input value="<?php echo $contestant_id; ?>" name="contestant_id" type="hidden" />
 
  <?php    
   	$cont_query = $conn->query("SELECT * FROM contestants WHERE contestant_id='$contestant_id'") or die(mysql_error());
    while ($cont_row = $cont_query->fetch()) 
        { ?> 
 
 
 
 <table align="center" style="width: 30% !important;">
 <tr>
 <td>
 

 <div style="width: 100% !important;" class="panel panel-primary">
            <div class="panel-heading">
              <h3 class="panel-title">Set Text Code</h3>
            </div>
 
 


 
     <div class="panel-body">
  
   <table align="center">
  
  
 
   <tr>
 
   <td>
    <strong>Text Code:</strong>
     <br />
   <input name="txt_code" type="text" class="form-control" placeholder="Enter Text Code" value="<?php echo $cont_row['txt_code']; ?>" />
   </td>
   
   </tr>

  <tr>
  <td >&nbsp;</td>
  </tr>
  <tr>
  <td align="right"><a href="sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>" class="btn btn-default">Back</a>&nbsp;<button name="edit_contestant" class="btn btn-success">Update</button></td>
  </tr>
  </table>
 
</div>
 
          </div>
  </td>
 </tr>
 </table>  
  <?php } ?> 
  
</form>

</div>

</div>       
          
<?php 

if(isset($_POST['edit_contestant']))
{
    
    $se_name=$_POST['se_name'];
    $sub_event_id=$_POST['sub_event_id'];
    $contestant_id=$_POST['contestant_id'];
    
     $txt_code=$_POST['txt_code'];
  
   /* contestants */
   
   
$ssquery = $conn->query("select * from contestants where txt_code='$txt_code'") or die(mysql_error());
$ssnum_row = $ssquery->rowcount(); if( $ssnum_row > 0) { ?>

<script>
			                                      
window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
alert('Textcode: <?php echo $txt_code ?> already exist, try another. . . Thanks.');						

</script>

<?php 
            
}else{
$conn->query("update contestants set txt_code='$txt_code' where contestant_id='$contestant_id'");  
?>

<script>
			                                      
window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
alert('Textcode updated successfully!');						

</script>

<?php  } } ?>
  
  
<?php include('footer.php'); ?>

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
