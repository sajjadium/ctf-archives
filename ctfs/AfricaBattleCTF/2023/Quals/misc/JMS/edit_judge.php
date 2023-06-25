 

<!DOCTYPE html>
<html lang="en">
  
  <?php 
  include('header.php');
    include('session.php');
    
    
    $sub_event_id=$_GET['sub_event_id'];
    $se_name=$_GET['se_name'];
    $judge_id=$_GET['judge_id'];
     
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
 <input value="<?php echo $judge_id; ?>" name="judge_id" type="hidden" />
 
  
   <div class="col-lg-3">
   </div>
   <div class="col-lg-6">
 <div class="panel panel-primary">
            <div class="panel-heading">
              <h3 class="panel-title">Edit Judge</h3>
            </div>
 
 


 
     <div class="panel-body">
  
   <table align="center">
  
  
  <?php    
   	$judge_query = $conn->query("SELECT * FROM judges WHERE judge_id='$judge_id'") or die(mysql_error());
    while ($judge_row = $judge_query->fetch()) 
        { ?>
   <tr>
    
   <td>
   Judge no. <br />
   <select name="judge_ctr" class="form-control">
   <option><?php echo $judge_row['judge_ctr']; ?></option>
   
                    <?php 
                    
                    $n1=0;
                    
                    while($n1<4)
                    { 
                        $n1++;
                     
                    
                    $cont_query = $conn->query("SELECT * FROM judges WHERE judge_ctr='$n1' AND subevent_id='$sub_event_id'") or die(mysql_error());
                   
            
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
    Judge Fullname <br />
   <input name="fullname" type="text" class="form-control" value="<?php echo $judge_row['fullname']; ?>" /></td>
   <td>&nbsp;</td>
   <td>
    Type <br />
    <select class="form-control" name="jtype">
    <option><?php echo $judge_row['jtype']; ?></option>
    <option>Chairman</option>
    <option></option>
    </select>
   
   
   </tr>
  <?php } ?>
  <tr>
  <td colspan="5">&nbsp;</td>
  </tr>
  <tr>
  <td colspan="5" align="right"><a href="sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>" class="btn btn-default">Back</a>&nbsp;<button name="edit_judge" class="btn btn-success">Update</button></td>
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

if(isset($_POST['edit_judge']))
{
    
    $se_name=$_POST['se_name'];
    $sub_event_id=$_POST['sub_event_id'];
    $judge_id=$_POST['judge_id'];
    $judge_ctr=$_POST['judge_ctr'];
     $fullname=$_POST['fullname'];
     $jtype=$_POST['jtype'];
  
   /* judges */
   
    $conn->query("update judges set fullname='$fullname',judge_ctr='$judge_ctr', jtype='$jtype' where judge_id='$judge_id'");
   
  
 ?>
<script>
			                                      
			      								window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
			      							   	alert('Judge <?php echo $fullname; ?> updated successfully!');						
			      								</script>
<?php  
 
 
} ?>
  
  
<?php include('footer.php'); ?>

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
