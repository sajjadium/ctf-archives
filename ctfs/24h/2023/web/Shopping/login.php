<?php
   session_start();
   include("config.php");
   
   if (isset($_SESSION['user'])){
      header("Location: index.php");
   }

   $error = "";
   if($_SERVER["REQUEST_METHOD"] == "POST") {
      
      $username = mysqli_real_escape_string($db,$_POST['username']);
      $password = mysqli_real_escape_string($db,$_POST['password']); 
      
      $sql = "SELECT username FROM users WHERE BINARY username = '$username' and password = '$password'";
      
      $result = mysqli_query($db,$sql);
      
      
      if ($row = mysqli_fetch_assoc($result)) {
         $_SESSION['user'] = $row['username'];
         header("Location: index.php");
      } else {
         $error = "Your Login Name or Password is invalid";
      }

   }
?>
<html>
   
   <head>
      <title>Login Page</title>
      <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet"/>
      <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" rel="stylesheet"/>
      <link href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/6.1.0/mdb.min.css" rel="stylesheet"/>
   </head>
   
   <body>
	
      <div class="h-100 d-flex align-items-center justify-content-center">

         
               <form action="" method="post" class="form">
                 <div class="form-outline mb-4">
                  <label class="form-label" for="username">username</label> <br/>
                   <input style="background:#01acff" type="text" name="username" id="username" class="form-control" />
                   
                 </div>

                 <!-- Password input -->
                 <div class="form-outline mb-4">
                  <label class="form-label" for="password">Password</label><br/>
                   <input style="background:#01acff" type="password" id="password" name="password" class="form-control" />
                   
                 </div>
                 
                 <h3 style="color: red"><?php echo $error;?> </h3>

                 <!-- 2 column grid layout for inline styling -->
                 <div class="row mb-4">
                   <div class="col d-flex justify-content-center">
                     <!-- Checkbox -->
                     <div class="form-check">
                       <input class="form-check-input" type="checkbox" value="" id="form2Example31" checked />
                       <label class="form-check-label" for="form2Example31"> Remember me </label>
                     </div>
                   </div>
                 </div>

                 <!-- Submit button -->
                 <button type="submit" class="btn btn-primary btn-block mb-4">Sign in</button>

                 <!-- Register buttons -->
                 <div class="text-center">
                   <p>Not a member? <a href="/signup.php">Register</a></p>
                 </div>
               </form>

      </div> 
      

   </body>
</html>



