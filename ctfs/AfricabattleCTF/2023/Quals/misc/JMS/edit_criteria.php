 

<!DOCTYPE html>
<html lang="en">
  
  <?php 
  include('header.php');
    include('session.php');
    
    
    $sub_event_id=$_GET['sub_event_id'];
    $se_name=$_GET['se_name'];
    $crit_id=$_GET['crit_id'];
     
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
 <input value="<?php echo $crit_id; ?>" name="crit_id" type="hidden" />
 
  
   <div class="col-lg-3">
   </div>
   <div class="col-lg-6">
 <div class="panel panel-primary">
            <div class="panel-heading">
              <h3 class="panel-title">Edit Criteria</h3>
            </div>
 
 


 
     <div class="panel-body">
  
   <table align="center">
  
  
  <?php    
   	$crit_query = $conn->query("SELECT * FROM criteria WHERE criteria_id='$crit_id'") or die(mysql_error());
    while ($crit_row = $crit_query->fetch()) 
        { ?>
   <tr>
    
   <td>
   Criteria no. <br />
   <select name="crit_ctr" class="form-control">
   <option><?php echo $crit_row['criteria_ctr']; ?></option>
   
                    <?php 
                    
                    $n1=0;
                    
                    while($n1<8)
                    { 
                        $n1++;
                     
                    
                    $cont_query = $conn->query("SELECT * FROM criteria WHERE criteria_ctr='$n1' AND subevent_id='$sub_event_id'") or die(mysql_error());
                   
            
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
    Criteria <br />
   <input name="criteria" type="text" class="form-control" value="<?php echo $crit_row['criteria']; ?>" /></td>
   
   <td>&nbsp;</td>
   <td>
    Percentage <br />
    <select name="percentage" class="form-control"> 
    <option><?php echo $crit_row['percentage']; ?></option>
    <?php
  $n1=-1;
  while($n1<100)
  { $n1=$n1+1;
    
    ?>
    <option><?php echo $n1; ?></option>
  <?php } ?>
  </select>
  </td>
   </tr>
  <?php } ?>
  
  <tr>
  <td colspan="5">&nbsp;</td>
  </tr>
  <tr>
  <td colspan="5" align="right"><a href="sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>" class="btn btn-default">Back</a>&nbsp;<button name="edit_crit" class="btn btn-success">Update</button></td>
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

if(isset($_POST['edit_crit']))
{
    
    $se_name=$_POST['se_name'];
    $sub_event_id=$_POST['sub_event_id'];
    $crit_id=$_POST['crit_id'];
    $percentage=$_POST['percentage'];
    $crit_ctr=$_POST['crit_ctr'];
     $criteria=$_POST['criteria'];
  
   /* judges */
   
    $conn->query("update criteria set criteria='$criteria',criteria_ctr='$crit_ctr', percentage='$percentage' where criteria_id='$crit_id'");
   
  
 ?>
<script>
			                                      
			      								window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
			      							   	alert('Criteria <?php echo $criteria; ?> updated successfully!');						
			      								</script>
<?php  
 
 
} ?>
  
  
<?php include('footer.php'); ?>

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
