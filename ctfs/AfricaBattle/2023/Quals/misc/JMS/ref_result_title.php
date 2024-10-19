<!DOCTYPE html>
<html lang="en">





<br /><br /><br /><br /><br /><br /><br />

<center>
<h3>* * * Loading Results  * * *</h3>
</center>
<br /><br /><br /><br /><br /><br /><br />

<?php

include('header2.php');
include('session.php');
   
   
   
   
$active_sub_event=$_GET['event_id'];
 
 
 
$j_query = $conn->query("select * from judges where subevent_id='$active_sub_event'") or die(mysql_error());
while ($j_row = $j_query->fetch()) 
{

$judge_id=$j_row['judge_id'];
         
        $s_event_query = $conn->query("select * from sub_event where subevent_id='$active_sub_event'") or die(mysql_error());
        while ($s_event_row = $s_event_query->fetch()) 
        {
    
                $i_rank_ctr=0;
                   
                $score_query = $conn->query("select * from sub_results where subevent_id='$active_sub_event' and judge_id='$judge_id' order by total_score DESC") or die(mysql_error());
                
                $num_rowxz = $score_query->rowcount();
            
                    if( $num_rowxz > 0 ) 
                    { 
                                while ($score_row = $score_query->fetch())
                                {
                                 
                                 
                                 
                                 $i_rank_ctr=$i_rank_ctr+1;
                             
                                 $last_rank_ctr=$i_rank_ctr-1;
                                 
                                 $rank=$score_row['rank'];
                                 $s_result_id=$score_row['subresult_id'];
                       
                              
                                 $i_rank_ctr;
                         
                                 $conn->query("update sub_results set rank='$i_rank_ctr' where subresult_id='$s_result_id'");
                                
                                
                                }  
                    }  
        } 
}?>
       
 

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
<?php  
    function ordinal($i)
    {
        $l = substr($i,-1);
        $s = substr($i,-2,-1);
        
        return (($l==1&amp;&amp;$s==1)||($l==2&amp;&amp;$s==1)||($l==3&amp;&amp;$s==1)||$l&gt;3||$l==0?'th':($l==3?'rd':($l==2?'nd':'st')));
    }   
    $s_event_query = $conn->query("select * from sub_event where subevent_id='$active_sub_event'") or die(mysql_error());
    while ($s_event_row = $s_event_query->fetch()) 
    {
            
                $MEidxx=$s_event_row['mainevent_id'];
            
                $event_query = $conn->query("select * from main_event where mainevent_id='$MEidxx'") or die(mysql_error());
        		while ($event_row = $event_query->fetch()) 
                {
            
           
        
                    $o_result_query = $conn->query("select distinct contestant_id from sub_results where mainevent_id='$MEidxx' and subevent_id='$active_sub_event' order by place_title, rank ASC") or die(mysql_error());
                    while ($o_result_row = $o_result_query->fetch()) 
                    {
                        
                    $contestant_id=$o_result_row['contestant_id'];
                     
                     
                    $rank_score=0;
 
 


                        $tot_score_query = $conn->query("select judge_id,total_score, deduction, rank from sub_results where contestant_id='$contestant_id'") or die(mysql_error());
                        while ($tot_score_row = $tot_score_query->fetch()) 
                        {
                        $rank_score=$rank_score+$tot_score_row['rank'];
                        } 
      
        
                            $rsChecker = $conn->query("select * from rank_system WHERE subevent_id='$active_sub_event' AND contestant_id='$contestant_id'") or die(mysql_error());
                            
                            if($rsChecker->rowCount()>0)
                            {
                                $conn->query("UPDATE rank_system SET total_rank='$rank_score' WHERE subevent_id='$active_sub_event' AND contestant_id='$contestant_id'"); 
                            }
                            else
                            {
                                $conn->query("insert into rank_system(subevent_id,contestant_id,total_rank)VALUES('$active_sub_event','$contestant_id','$rank_score')"); 
                            }
        
         


          
                                  $rspCtr=0;
                                  $rsPlacer = $conn->query("SELECT * FROM rank_system WHERE subevent_id='$active_sub_event' ORDER BY total_rank ASC") or die(mysql_error());
                                  while ($rsp_row = $rsPlacer->fetch()) 
                                  {
                                    $rspCtr++;
                                    
                                    $rsp_contestant_id=$rsp_row['contestant_id'];
                                    $conn->query("UPDATE sub_results SET place_title='".(ordinal($rspCtr))."' WHERE contestant_id='$rsp_contestant_id'"); 
                                    // if($rspCtr==1)
                                    // {
                                    //     $conn->query("UPDATE sub_results SET place_title='1st' WHERE contestant_id='$rsp_contestant_id'"); 
                                    // }
                                    
                                    
                                    // if($rspCtr==2)
                                    // {
                                    //     $conn->query("UPDATE sub_results SET place_title='2nd' WHERE contestant_id='$rsp_contestant_id'"); 
                                    // }
                                    
                                    
                                    // if($rspCtr==3)
                                    // {
                                    //     $conn->query("UPDATE sub_results SET place_title='3rd' WHERE contestant_id='$rsp_contestant_id'"); 
                                    // }
                                    
                                    
                                    // if($rspCtr>3)
                                    // {
                                    //     $conn->query("UPDATE sub_results SET place_title='4th' WHERE contestant_id='$rsp_contestant_id'"); 
                                    // }
                                    
                                  }



                    } 
            } 
    } ?>
 

    <?php include('footer.php'); ?>
 



    <script>
    window.location='result_title.php?event_id=<?php echo $active_sub_event; ?>&refRT=ok';
    </script>
   
   
  </body>
</html>
