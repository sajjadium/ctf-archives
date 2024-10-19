 

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
    <p class="lead">Judging Management System</p>
  </div>
</header>
    <div class="container">

   <form method="POST">
    <input value="<?php echo $sub_event_id; ?>" name="sub_event_id" type="hidden" />
 <input value="<?php echo $se_name; ?>" name="se_name" type="hidden" />
 <input value="<?php echo $contestant_id; ?>" name="contestant_id" type="hidden" />
 
  
   <div class="col-lg-3">
   </div>
   <div class="col-lg-6">
 <div class="panel panel-primary">
            <div class="panel-heading">
              <h3 class="panel-title">Edit Contestant</h3>
            </div>
 
 


 
     <div class="panel-body">
  
   <table align="center">
  
  
  <?php    
   	$cont_query = $conn->query("SELECT * FROM contestants WHERE contestant_id='$contestant_id'") or die(mysql_error());
    while ($cont_row = $cont_query->fetch()) 
        { ?>
   <tr>
    
   <td>
   Contestant no. <br />
   <select name="contestant_ctr" class="form-control">
   <option><?php echo $cont_row['contestant_ctr']; ?></option>
   
                    <?php 
                    
                    $n1=0;
                    
                    while($n1<12)
                    { 
                        $n1++;
                     
                    
                    $cont_query = $conn->query("SELECT * FROM contestants WHERE contestant_ctr='$n1' AND subevent_id='$sub_event_id'") or die(mysql_error());
                   
            
                    if($cont_query->rowCount()>0)
                    {
                        
                    }
                    else
                    {
                        echo "<option>".$n1."</option>";
                    }
                      
                    } 
                    
                    ?>
 
   </select></td>
   <td>&nbsp;</td>
   <td>
    Contestant Fullname <br />
   <input name="fullname" type="text" class="form-control" value="<?php echo $cont_row['fullname']; ?>" /></td>
   </tr>
  <?php } ?>
  <tr>
  <td colspan="3">&nbsp;</td>
  </tr>
  <tr>
  <td colspan="3" align="right"><a href="sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>" class="btn btn-default">Back</a>&nbsp;<button name="edit_contestant" class="btn btn-success">Update</button></td>
  </tr>
  </table>
 
</div>
 
          </div>
          
        
  </div>
  
 <div class="col-lg-3">
   </div>
 
</form>
          </div>
          
          
<?php 

if(isset($_POST['edit_contestant']))
{
    
    $se_name=$_POST['se_name'];
    $sub_event_id=$_POST['sub_event_id'];
    $contestant_id=$_POST['contestant_id'];
    $contestant_ctr=$_POST['contestant_ctr'];
     $fullname=$_POST['fullname'];
  
   /* contestants */
   
    $conn->query("update contestants set fullname='$fullname',contestant_ctr='$contestant_ctr' where contestant_id='$contestant_id'");
   
  
 ?>
<script>
			                                      
			      								window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
			      							   	alert('Contestant <?php echo $fullname; ?> updated successfully!');						
			      								</script>
<?php  
 
 
} ?>
  
  
<?php include('footer.php'); ?>


    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
