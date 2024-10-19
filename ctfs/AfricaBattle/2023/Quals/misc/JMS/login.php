<?php
		include('dbcon.php');
		session_start();
		$username = $_POST['username'];
		$password = $_POST['password'];
		/* student */
			$query = $conn->query("SELECT * FROM organizer WHERE username='$username' AND password='$password'");
			$row = $query->fetch();
			$num_row = $query->rowcount();
		if( $num_row > 0 ) { 
		  
	 if($row['access']=="Organizer")
     {
        $_SESSION['useraccess']="Organizer";
        $_SESSION['id']=$row['organizer_id'];
        
        ?>	<script>window.location = 'selection.php';</script><?php
        	
     }
     else
     {
        
        $_SESSION['useraccess']="Tabulator";
        $_SESSION['id']=$row['org_id'];
        $_SESSION['userid']=$row['organizer_id'];
        
        ?>	<script>window.location = 'score_sheets.php';</script><?php
        	
     }
        
		}else{ 
			?>	<script>
              alert('Username and Password did not Match');
			  window.location = 'index.php';
			    </script><?php	
		}	
				
		?>
        