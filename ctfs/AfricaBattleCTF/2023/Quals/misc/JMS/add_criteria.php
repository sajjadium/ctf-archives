 

<!DOCTYPE html>
<html lang="en">
  
  <?php 
  include('header.php');
    include('session.php');
    
    
    $sub_event_id=$_GET['sub_event_id'];
    $se_name=$_GET['se_name'];
    
     
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

<div class="span12">



                <br />
                <div class="col-md-12">
                    <ul class="breadcrumb">
                    
                        <li><a href="selection.php">User Selection</a></li>
                    
                        <li><a href="home.php">List of Events</a></li>
                        
                        <li><a href="sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id; ?>&se_name=<?php echo $se_name; ?>"><?php echo $se_name; ?> Settings</a></li>
                        
                        <li>Add Criteria</li>
                        
                    </ul>
                </div>


                
                
                
   <form method="POST">
    <input value="<?php echo $sub_event_id; ?>" name="sub_event_id" type="hidden" />
 <input value="<?php echo $se_name; ?>" name="se_name" type="hidden" />
 
 
  
<table align="center" style="width: 45% !important;">
 <tr>
 <td>
 

 <div style="width: 100% !important;" class="panel panel-primary">
 
            <div class="panel-heading">
              <h3 class="panel-title">Add Criteria</h3>
            </div>
 
     <div class="panel-body">
  
   <table align="center">
  
  
  
   <tr>
    
   <td>
   <strong>Criteria no. :</strong> <br />
   <select name="crit_ctr" class="form-control">
   
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
    <strong>Criteria:</strong> <br />
   <input name="criteria" type="text" class="form-control" placeholder="Criteria Description"   /></td>
   
   <td>&nbsp;</td>
   <td>
    <strong>Percentage:</strong> <br />
    <select name="percentage" class="form-control"> 
   
    <?php
  $n1=0;
  while($n1<100)
  { $n1=$n1+1;
    
    ?>
    <option><?php echo $n1; ?></option>
  <?php } ?>
  </select>
  </td>
   </tr>
  
  
  <tr>
  <td colspan="5">&nbsp;</td>
  </tr>
  <tr>
  <td colspan="5" align="right"><a href="sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>" class="btn btn-default">Back</a>&nbsp;<button name="add_crit" class="btn btn-success">Save</button></td>
  </tr>
  </table>
 </form>
</div>
 
          </div>
 
 
 </td>
 </tr>
 </table> 
 

</div>
          
</div>
          
          
<?php 

if(isset($_POST['add_crit']))
{
    
    $se_name=$_POST['se_name'];
    $sub_event_id=$_POST['sub_event_id'];
    
    $percentage=$_POST['percentage'];
    $crit_ctr=$_POST['crit_ctr'];
     $criteria=$_POST['criteria'];
  
   /* criteria */
   
      $conn->query("insert into criteria(criteria,subevent_id,criteria_ctr,percentage)values('$criteria','$sub_event_id','$crit_ctr','$percentage')");
  
 ?>
<script>
			                                      
			      								window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
			      							   	alert('Criteria <?php echo $criteria; ?> added successfully!');						
			      								</script>
<?php  
 
 
} ?>
  
  <?php include('footer.php'); ?>


    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
