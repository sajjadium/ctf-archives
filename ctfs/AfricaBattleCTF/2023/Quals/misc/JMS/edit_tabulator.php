
<!DOCTYPE html>
<html lang="en">

    <?php 
    include('header.php');
     include('session.php');
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
    <h1>Settings - Tabulator</h1>
    <p class="lead">Judging Management System</p>
  </div>
</header>


    <div class="container">
 
 
 
    <div class="col-lg-3">  </div>
 
 
 
  <div class="col-lg-6">
  
 <a href="edit_organizer.php" class="btn btn-primary"><strong>ORGANIZER SETTINGS &raquo;</strong></a>
  
 
 <hr />
 
 <div class="panel panel-danger">
            <div class="panel-heading">
              <h3 class="panel-title"><strong>Tabulator Settings Panel</strong></h3>
            </div>
            
            
            
            <div class="panel-body">
    
 
    
     <form method="POST" enctype="multipart/form-data"> 
   <?php 
       $query = $conn->query("select * from organizer where org_id='$session_id'") or die(mysql_error());
		
        if($query->rowCount()>0)
        {
 
        while ($row = $query->fetch()) 
        { ?>
            
       
        
       
        
    <table align="center">
     <tr><td colspan="5"><strong>Basic Information</strong><hr /></td></tr>
    <tr>
    <td>
    Firstname:
    <input type="text" name="fname" class="form-control" placeholder="Firstname" value="<?php echo $row['fname']; ?>" aria-describedby="basic-addon1" required autofocus>
 </td>
    <td>&nbsp;</td>
    <td>
    Middlename:
    <input type="text" name="mname" class="form-control" placeholder="Middlename" value="<?php echo $row['mname']; ?>" aria-describedby="basic-addon1" required autofocus>
 </td>
    <td>&nbsp;</td>
    <td>
    Lastname:
    <input type="text" name="lname" class="form-control" placeholder="Lastname" value="<?php echo $row['lname']; ?>" aria-describedby="basic-addon1" required autofocus>
 </td>
    </tr>
    
     <tr><td colspan="5">&nbsp;</td></tr>
     
      <tr><td colspan="5"><strong>Account Security</strong><hr /></td></tr>
      
     <tr>
    <td>
    Username:
    <input type="text" name="username" class="form-control" placeholder="Username" value="<?php echo $row['username']; ?>" aria-describedby="basic-addon1" required autofocus>
 </td>
    <td>&nbsp;</td>
    <td>
    New Password:
    <input id="password" type="password" name="passwordx" class="form-control" placeholder="Password" value="<?php echo $row['password']; ?>" aria-describedby="basic-addon1" required autofocus>
 </td>
    <td>&nbsp;</td>
    <td>
    Re-type Password:
    <input id="confirm_password" type="password" name="password2x" class="form-control" placeholder="Re-type Password" value="<?php echo $row['password']; ?>" aria-describedby="basic-addon1" required autofocus>
 </td>
    </tr>
    <tr>
    <td colspan="4"></td>
    <td><span id='message'></span></td>
    </tr>
    <tr><td colspan="5">&nbsp;</td></tr>
    
    <tr><td colspan="5"><strong>Confirmation</strong><hr /></td></tr>
 
 
    <tr>
 
    <td colspan="5">
    Tabulator Current Password:
    <input type="password" name="tab_password" class="form-control" placeholder="Tabulator Current Password" aria-describedby="basic-addon1" required autofocus>
    </td>
     
    </tr>
    
    <tr>
    <td colspan="5">&nbsp;</td>
    </tr>
    
    <tr>
 
    <td colspan="5">
    Organizer Current Password:
    <input type="password" name="org_password" class="form-control" placeholder="Organizer Current Password" aria-describedby="basic-addon1" required autofocus>
    </td>
     
    </tr>
 
  
    </table>
   
   
   
   <div class="col-lg-12">
<hr />
       <div class="btn-group pull-right">
  <a href="home.php" type="button" class="btn btn-default">Cancel</a>
  <button name="update" type="submit" class="btn btn-success">Update</button>
   </div>
 </div> 
   
   </form>
   
   
      
       
       
       
       
           <?php }
           
           
           
            }
            else
            {
                
            ?>
       
       
       
 
            
   <form method="POST">

        
    <table align="center">
    <tr><td colspan="5"><strong>Basic Information</strong><hr /></td></tr>
    <tr>
    <td>
    Firstname:
    <input type="text" name="fname" class="form-control" placeholder="Firstname" aria-describedby="basic-addon1" required autofocus>
 </td>
    <td>&nbsp;</td>
    <td>
    Middlename:
    <input type="text" name="mname" class="form-control" placeholder="Middlename" aria-describedby="basic-addon1" required autofocus>
 </td>
    <td>&nbsp;</td>
    <td>
    Lastname:
    <input type="text" name="lname" class="form-control" placeholder="Lastname" aria-describedby="basic-addon1" required autofocus>
 </td>
    </tr>
    
    
     <tr><td colspan="5">&nbsp;</td></tr>
     
     <tr><td colspan="5"><strong>Account Security</strong><hr /></td></tr>
     
     <tr>
    <td>
    Username:
    <input type="text" name="username" class="form-control" placeholder="Username" aria-describedby="basic-addon1" required autofocus>
 </td>
    <td>&nbsp;</td>
    <td>
    Password:
    <input id="password" type="password" name="passwordx" class="form-control" placeholder="Password" aria-describedby="basic-addon1" required autofocus>
 </td>
    <td>&nbsp;</td>
    <td>
    Re-type Password:
    <input id="confirm_password" type="password" name="password2" class="form-control" placeholder="Re-type Password" aria-describedby="basic-addon1" required autofocus>
 </td>
    </tr>
    
   <tr>
    <td colspan="4"></td>
    <td><span id='message'></span></td>
    </tr> 
    
    
    
         <tr><td colspan="5">&nbsp;</td></tr>
     <tr><td colspan="5"><strong>Confirmation</strong><hr /></td></tr>
     <tr>
 
    <td colspan="5">
    Organizer Password:
    <input type="password" name="org_password" class="form-control" placeholder="Password" aria-describedby="basic-addon1" required autofocus>
 </td>
    
    </tr>
    </table>
 <br />
 
 
       <div class="btn-group pull-right">
  <a href="edit_organizer.php" type="button" class="btn btn-default">CANCEL</a>
  <button name="add_tabulator" type="submit" class="btn btn-primary">ADD</button>
  </div>
  
  
   </form>
 
  <?php } ?>
  
  


  
            </div><!-- end panel body -->
          </div> <!-- end panel -->
  </div><!-- end col-6 -->
  
   <div class="col-lg-3">  </div>
   
</div> <!-- end container -->
          
          
   <?php include('footer.php'); ?>


    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="javascript/jquery1102.min.js"></script>
    <script src="../assets/js/ie10-viewport-bug-workaround.js"></script>
    
    
    <script>
 
    $('#password, #confirm_password').on('keyup', function () {
      if ($('#password').val() == $('#confirm_password').val()) {
        $('#message').html('Matching').css('color', 'green');
      } else 
        $('#message').html('Not Matching').css('color', 'red');
    });
    
    </script>
    
  </body>
</html>
 
    
    
<?php 


if(isset($_POST['add_tabulator']))
{
 
   $fname=$_POST['fname']; 
   $mname=$_POST['mname'];  
   $lname=$_POST['lname'];  
   
   $username=$_POST['username'];  
   $password=$_POST['passwordx'];  
   $password2=$_POST['password2'];  
  
   $org_password=$_POST['org_password']; 
   
  
 if($password==$password2)
 {
 
 if($org_password==$check_pass)
 {
  
  $org_query = $conn->query("SELECT * FROM organizer WHERE password='$org_password' AND access='Organizer'");
			$org_row = $org_query->fetch();
			$org_num_row = $org_query->rowcount();
		if( $org_num_row > 0 ) 
        { 
 
     $active_sub_event=$org_row['active_sub_event'];
     		
     
      $conn->query("insert into organizer(fname,mname,lname,username,password,org_id,access,status)
      values('$fname','$mname','$lname','$username','$password','$session_id','Tabulator','offline')");

        ?>	
        <script>
        alert('Tabulator <?php echo $fname; ?> successfully added...');
        window.location = 'edit_tabulator.php';
		</script>
        <?php }else{ ?>	
        <script>
        alert('Confirmation Password error... Pls. contact event organizer.');
        window.location = 'edit_tabulator.php';
		</script><?php	
		}
    
 }
 
 }
 else
 {
  ?>
  
  
<script>
alert('Tabulator <?php echo $fname." ".$mname." ".$lname; ?> registration cannot be done. Password and Re-typed password did not match.');						
</script>


<?php  
 }
 
} ?>