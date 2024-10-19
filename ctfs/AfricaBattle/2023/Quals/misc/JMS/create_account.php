
<!DOCTYPE html>
<html lang="en">

    <?php 
    include('header.php');
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
    <h1>Account Registration</h1>
    <p class="lead">Judging Management System</p>
  </div>
</header>
    <div class="container">

  <div class="col-lg-3">
 
  </div>
  <div class="col-lg-6">
 <div class="panel panel-primary">
            <div class="panel-heading">
              <h3 class="panel-title">Event Organizer Registration Form</h3>
            </div>
            <div class="panel-body">
            
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
    <input id="password" type="password" name="password" class="form-control" placeholder="Password" aria-describedby="basic-addon1" required="true" autofocus="true" />
 </td>
    <td>&nbsp;</td>
    <td>
    Re-type Password:
    <input id="confirm_password" type="password" name="password2" class="form-control" placeholder="Re-type Password" aria-describedby="basic-addon1" required="true" autofocus="true" />
 </td>
    </tr>
    
    <tr>
    <td colspan="4">&nbsp;</td>
    <td><span id='message'></span></td>
    </tr>
    
    
    </table>
 <br />
       <div class="btn-group pull-right">
  <a href="index.php" type="button" class="btn btn-default">Cancel</a>
  <button name="register" type="submit" class="btn btn-primary">Register</button>
   </form>
</div>
 
    
            </div>
          </div>
  </div>
  <div class="col-lg-3">
 
  </div>
 
          </div>
          
    <!-- Footer
    ================================================== -->
    <footer class="footer">
      <div class="container">
 
        <font size="2" class="pull-left"><strong>Judging Management System &middot; &COPY; <?= date ("Y") ?></strong> </font> <br />
       
      </div>
    </footer>      
   


    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../assets/js/ie10-viewport-bug-workaround.js"></script>
    <script src="javascript/jquery1102.min.js"></script>
    
    
    
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

if(isset($_POST['register']))
{
 
   $fname=$_POST['fname']; 
   $mname=$_POST['mname'];  
   $lname=$_POST['lname'];  
   
   $username=$_POST['username'];  
   $password=$_POST['password'];  
   $password2=$_POST['password2'];  
  
 if($password==$password2)
 {
  $conn->query("insert into organizer(fname,mname,lname,username,password,access,status)values('$fname','$mname','$lname','$username','$password','Organizer','offline')");

 ?>
<script>
			                                      
			      								window.location = 'index.php';
			      							   	alert('Organizer <?php echo $fname." ".$mname." ".$lname; ?> registered successfully!');						
			      								</script>
<?php  
 }
 else
 {
  ?>
<script>
 
			      							   	alert('Organizer <?php echo $fname." ".$mname." ".$lname; ?> registration cannot be done. Password and Re-typed password did not match.');						
			      								</script>
<?php  
 }
 
} ?>

 
