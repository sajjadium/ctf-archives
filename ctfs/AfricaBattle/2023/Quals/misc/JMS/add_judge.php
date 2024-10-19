 

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
                        
                        <li>Add Judge</li>
                        
                    </ul>
                </div>
                

   <form method="POST">
   <input value="<?php echo $sub_event_id; ?>" name="sub_event_id" type="hidden" />
 <input value="<?php echo $se_name; ?>" name="se_name" type="hidden" />
 
  
<table align="center" style="width: 40% !important;">
 <tr>
 <td>
 

 <div style="width: 100% !important;" class="panel panel-primary">
 
            <div class="panel-heading">
              <h3 class="panel-title">Add Judge</h3>
            </div>
 
 


 
     <div class="panel-body">
 
   <table align="center">
  
 
   <tr>
    
   <td>
   <strong>Judge no. :&nbsp;&nbsp;&nbsp;</strong><br />
   <select name="judge_ctr" class="form-control">
   

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
   <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
   <td>
    <strong>Judge Fullname:</strong> <br />
   <input name="fullname" placeholder="Enter Judge Name" type="text" class="form-control" required="true" /></td>
   </tr>
  
  <tr>
  <td colspan="3">&nbsp;</td>
  </tr>
  
  <tr>
  <td colspan="3" align="right"><a href="sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>" class="btn btn-default">Back</a>&nbsp;<button name="add_judge" class="btn btn-primary">Save</button></td>
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

if(isset($_POST['add_judge']))
{
    
function randomcode() {
$var = "abcdefghijkmnopqrstuvwxyz0123456789";
srand((double)microtime()*1000000);
$i = 0;
$code = '' ;
while ($i <= 5) {
$num = rand() % 33;
$tmp = substr($var, $num, 1);
$code = $code . $tmp;
$i++;
}
return $code;
}
    
$se_name=$_POST['se_name'];
$sub_event_id=$_POST['sub_event_id'];
$judge_ctr=$_POST['judge_ctr'];
$fullname=$_POST['fullname'];
$code=randomcode();

   /* judges */
   
    $conn->query("insert into judges(fullname,subevent_id,judge_ctr,code)values('$fullname','$sub_event_id','$judge_ctr','$code')");
   
  
 ?>
<script>
window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
alert('Judge <?php echo $fullname; ?> added successfully!');
</script>
<?php  
 
 
} ?>
  
<?php include('footer.php'); ?>

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../assets/js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
