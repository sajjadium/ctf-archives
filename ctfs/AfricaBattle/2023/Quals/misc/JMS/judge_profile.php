<?php 
include('session.php');

$judge_code=$_POST['judge_code'];

	$query = $conn->query("SELECT * FROM judges WHERE code='$judge_code'");
			$row = $query->fetch();
			$num_row = $query->rowcount();
            
            
            
            
		if( $num_row > 0 ) { 
		  
          
$judge_ctr=$row['judge_ctr'];
$subevent_id=$row['subevent_id'];

?>

            <script>
            
            window.location.href = "judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>";
            </script>
<?php }
else
{ ?>

<script>
alert('wrong code');
 			
window.location = 'selection.php';
</script>
    
<?php }
?>


                                                