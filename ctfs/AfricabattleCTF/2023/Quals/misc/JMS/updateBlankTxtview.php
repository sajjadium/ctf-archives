<?php

   include('header2.php');
    include('session.php');
    
    $get_sid=$_GET['sid'];
    
    
    $conn->query("update sub_event set txtpollview='deactivated'");
    
    $conn->query("update sub_event set txtpollview='activated' where subevent_id='$get_sid'");
   
  
 ?>
 
 
<script>
window.location = 'view_blanktxtpoll.php';
</script>
 