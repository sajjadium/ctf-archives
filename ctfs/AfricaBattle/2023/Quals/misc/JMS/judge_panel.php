 
<!DOCTYPE html>
<html lang="en">
 
  <?php
  error_reporting(0);
   include('header2.php');
    include('session.php');
    $judge_ctr=$_GET['judge_ctr'];
    $subevent_id=$_GET['subevent_id'];
    $getContestant_id=$_GET['contestant_id'];
    $pageStat=$_GET['pStat'];
   
    ?>

  <?php    $event_query = $conn->query("select * from sub_event where subevent_id='$subevent_id'") or die(mysql_error());
		while ($event_row = $event_query->fetch()) 
        { ?>
 
             <?php
             $se_MEidxx=$event_row['mainevent_id'];
             $se_namexx=$event_row['event_name'];
             $se_statusxx=$event_row['status'];
              ?> 
 
 <?php } ?>
<?php    
 
 if($se_statusxx=="activated")
 {
 
 
 $judge_query = $conn->query("select * from judges where subevent_id='$subevent_id' and judge_ctr='$judge_ctr'") or die(mysql_error());
		
        	$num_row = $judge_query->rowcount();
		      if( $num_row > 0 ) 
              {
                
                 while ($judge_row = $judge_query->fetch()) 
        {
            $j_id=$judge_row['judge_id']; 
          $j_name=$judge_row['fullname'];
          $j_code=$judge_row['code'];
           $jtype=$judge_row['jtype'];
            ?>
 
<?php } }}?>
         
         
  <body>

    <!-- Navbar
    ================================================== -->
    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
               <a class="brand" href="#"><img src="uploads/<?php echo $company_logo; ?>" width="23" height="23" />&nbsp; <font size="3">Judging Management System</font></a>
          <div class="nav-collapse collapse">
            <ul class="nav">
 
              <li>
                <a href="selection.php">&laquo; Back to <i><strong>User Selection Panel</strong></i></a>
              </li>
              
           
              
                <li>
                <a href="#">   
                <font color="white">Event: <strong><?php echo $se_namexx; ?></strong></font>  
                </a>
              </li>
              
                <li>
                <a href="#">
                <font color="white">Judge: <strong><?php echo $j_name; ?>&nbsp;&nbsp;&nbsp;<?php echo $jtype; ?> </strong></font>
                </a>
              </li>
              
              
      
            </ul>
          </div>
 
        </div>
      </div>
    </div>
 

<!-- Subhead
================================================== -->
 <?php    
 
 if($se_statusxx=="activated")
 {
 

 $judge_query = $conn->query("select * from judges where subevent_id='$subevent_id' and judge_ctr='$judge_ctr'") or die(mysql_error());
		
        	$num_row = $judge_query->rowcount();
		      if( $num_row > 0 ) 
              {
                
                 while ($judge_row = $judge_query->fetch()) 
        {
            $j_id=$judge_row['judge_id']; 
          $j_name=$judge_row['fullname'];
          $j_code=$judge_row['code'];
            ?>
          
          
<!-- Subhead
================================================== -->
<table style="background-color: #30475E; width: 100% !important; height: 150px; text-indent: 25px;" align="center" border="0">
<tr>
<td>
<h1 style="color: whitesmoke !important;">Judge's Panel</h1>
<h4 style="color: whitesmoke !important;">Judging Management System</h4>
</td>
</tr>
</table>
 


         <br />
        <?php } } } else { $j_name="Event is still inactive. Please contact the Event Organizer."; ?>


<table style="background-color: #30475E; width: 100% !important; height: 150px; text-indent: 25px;" align="center" border="0">
<tr>
<td>
<h1 style="color: whitesmoke !important;">Judge's Panel - <font color="red"><?php echo $j_name; ?></font></h1>
<h4 style="color: whitesmoke !important;">Judging Management System</h4>
</td>
</tr>
</table>
 
<?php
 }
         ?>



  <div class="container">
   <div class="row">
    <div class="span12">
 
  
        
<?php   if( $num_row > 0 ) { ?>
 
<ul class="nav nav-tabs alert-success">
 
<?php

    
if($pageStat=="Change")
{ 
    $cont_query = $conn->query("select * from contestants where subevent_id='$subevent_id' AND contestant_id='$getContestant_id'") or die(mysql_error());
while ($cont_row = $cont_query->fetch()) { 
     
    ?>

     <li><a><strong>Change Score Panel - <?php echo $cont_row['fullname']; ?></strong></a></li>
 
<?php }}
else
{
    $cont_query = $conn->query("select * from contestants where subevent_id='$subevent_id' order by contestant_ctr") or die(mysql_error());
while ($cont_row = $cont_query->fetch()) { 
    $con_idTab=$cont_row['contestant_id'];
    
    ?>
  
<?php    

    ?>
    <?php if($getContestant_id==$con_idTab){?>
        <li class="active" ><a href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=<?php echo $con_idTab;?>"><strong><?php echo $cont_row['fullname']; ?></strong></a></li>
    <?php }else{  ?>
            <li class="" ><a href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=<?php echo $con_idTab;?>"><?php echo $cont_row['fullname']; ?></a></li>
   
    <?php }} ?>
    
    <?php if($getContestant_id=="allTally"){?>
    <li class="active" ><a href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=allTally"><strong>View Tally</strong></a></li>
      <li><a href="selection.php"><strong><font color="red">Exit</font></strong></a></li>
    <?php }else{ ?>
        
        <li class="" ><a href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=allTally">View Tally</a></li>
      
    <?php   } ?>
      
     
  


<?php   } ?>

</ul> 

<?php
if($getContestant_id=="allTally")
{ ?>
               
 
                        <table align="center" class="table table-bordered">
                         
                        <tr>
                        <td align="center" colspan="5">
                        
                        <center>
                        <h3><strong><?php echo $se_namexx; ?></strong></h3> 
                        <p><strong class="aleret alert-danger">In case of tie, please break the tie by clicking the change button and change the scores.</strong></p>
                        </center>
                        
                        </td>
                        </tr>
                        
                        <tr>
                        <td><center>Contestant Name</center></td>
                        <td><center>Scoresheet</center></td>
                        <td style="background:#e4f6e2"><center>Final Score</center></td>
                        <td bgcolor="green"><center><font color="white">Rank</font></center></td>
                        <td>&nbsp;</td>
                        </tr>
                         
                        <?php 
                        $rankCtr=0;
                        
                        
                        $score_queryzz = $conn->query("select DISTINCT contestant_id from sub_results where subevent_id='$subevent_id' AND judge_id='$j_id' ORDER BY total_score DESC") or die(mysql_error());
                        while ($cont_row = $score_queryzz->fetch())
                         {
                         
                         $rankCtr=$rankCtr+1;
                         
                            $conID=$cont_row['contestant_id'];
                            
                        $score_query = $conn->query("select * from sub_results where contestant_id='$conID' AND judge_id='$j_id'") or die(mysql_error());
                        while ($score_row = $score_query->fetch())
                         {
                             $s1=$score_row['criteria_ctr1'];
                             $s2=$score_row['criteria_ctr2'];
                             $s3=$score_row['criteria_ctr3'];
                             $s4=$score_row['criteria_ctr4'];
                             $s5=$score_row['criteria_ctr5'];
                             $s6=$score_row['criteria_ctr6'];
                             $s7=$score_row['criteria_ctr7'];
                             $s8=$score_row['criteria_ctr8'];
                             $s9=$score_row['criteria_ctr9'];
                             $s10=$score_row['criteria_ctr10'];
                             $comments=$score_row['comments'];
                         }
                            
                            ?>
                           
                        <tr>
                        
                        <td align="center">
                       
                        <strong>
                        <?php
                        $contzx_query = $conn->query("select fullname from contestants where contestant_id='$conID'");
                        $contzx_row=$contzx_query->fetch();
                        echo $contzx_row['fullname'];
                        ?>
                        </strong>
                       
                        </td>
                            
                        <td align="center">
                            
                        <table align="center" class="table table-bordered">
                        <tr>
                         <?php   
                        
                        $totzxzxzxzxz=0;
                        
                        $criteria_query = $conn->query("select * from criteria where subevent_id='$subevent_id' order by criteria_ctr ASC") or die(mysql_error());
                        while ($crit_row = $criteria_query->fetch()) { 
                            
                            $totzxzxzxzxz=$crit_row['percentage']+$totzxzxzxzxz;
                            }
                            ?>
                            
                            
                        <?php
                        
                        
                        $criteria_query = $conn->query("select * from criteria where subevent_id='$subevent_id' order by criteria_ctr ASC") or die(mysql_error());
                        while ($crit_row = $criteria_query->fetch()) {
                        
                        ?>
                        
                        <td><center><font size="2"><?php echo $crit_row['criteria']." - ".$crit_row['percentage']."%";?></font></center></td>
                         
                        <?php } ?>
                         </tr>
                         
                        <tr>
                        <?php   
                        
                        $totzxzxzxzxz=0;
                        
                        $criteria_query = $conn->query("select * from criteria where subevent_id='$subevent_id' order by criteria_ctr ASC") or die(mysql_error());
                        while ($crit_row = $criteria_query->fetch()) { 
                            
                            $totzxzxzxzxz=$crit_row['percentage']+$totzxzxzxzxz;
                            }
                            ?>
                            
                            
                        <?php
                        
                        
                        $criteria_query = $conn->query("select * from criteria where subevent_id='$subevent_id' order by criteria_ctr ASC") or die(mysql_error());
                        while ($crit_row = $criteria_query->fetch()) {
                            
                        
                            
                            ?>
                         
                        <td align="center" bgcolor="#C5EAF9">
                         
                         
                         <?php
                         if($crit_row['criteria_ctr']==1)
                         { ?>
                            <?php echo $s1; ?>
                        <?php } ?>
                        
                        
                         <?php
                         if($crit_row['criteria_ctr']==2)
                         { ?>
                          <?php echo $s2; ?>
                        <?php } ?>
                        
                        
                         <?php
                         if($crit_row['criteria_ctr']==3)
                         { ?>
                        <?php echo $s3; ?>
                        <?php } ?>
                        
                        
                         <?php
                         if($crit_row['criteria_ctr']==4)
                         { ?>
                        <?php echo $s4; ?>
                        <?php } ?>
                        
                        
                         <?php
                         if($crit_row['criteria_ctr']==5)
                         { ?>
                        <?php echo $s5; ?>
                        
                        <?php } ?>
                        
                         
                          <?php
                         if($crit_row['criteria_ctr']==6)
                         { ?>
                        <?php echo $s6; ?>
                        
                        <?php } ?>
                        
                        
                        
                        <?php
                         if($crit_row['criteria_ctr']==7)
                         { ?>
                        <?php echo $s7; ?>
                        
                        <?php } ?>
                        
      
                          
                          
                          </td>
                         
                        
                        <?php } ?>
                        </tr>
                         
                        
                        </table>
                        <font size="2"><strong>Comment:</strong> <?php echo $comments; ?></font>
                        
                        </td>
                        

<!-- auto ranking --><!-- auto ranking --><!-- auto ranking --><!-- auto ranking --><!-- auto ranking --><!-- auto ranking --><!-- auto ranking --><!-- auto ranking --><!-- auto ranking --><!-- auto ranking -->
                            
                        <?php
                           
                        $score_query = $conn->query("select * from sub_results where subevent_id='$subevent_id' and judge_id='$j_id' and contestant_id='$conID' ORDER BY total_score DESC") or die(mysql_error());
                        while ($score_row = $score_query->fetch()) 
                        { 
                            
                                $myScore=$score_row['total_score'];
                                     
                                     
                                $scoreCHK_query = $conn->query("select * from sub_results where subevent_id='$subevent_id' and judge_id='$j_id' and total_score='$myScore' AND judge_rank_stat=''") or die(mysql_error());
                                
                                
                                
                                //start of Tie ctr #1
                                
                                
                                if($rankCtr==1 AND $scoreCHK_query->rowcount()==2)
                                {
                                    
                                    $newRank=3/2;
                             
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                          
                                }
                                elseif($rankCtr==1 AND $scoreCHK_query->rowcount()==3)
                                {
                                    
                                    $newRank=6/3;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                  
                                }
                                elseif($rankCtr==1 AND $scoreCHK_query->rowcount()==4)
                                {
                                    
                                    $newRank=10/4;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==1 AND $scoreCHK_query->rowcount()==5)
                                {
                                    
                                    $newRank=15/5;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==1 AND $scoreCHK_query->rowcount()==6)
                                {
                                    
                                    $newRank=21/6;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==1 AND $scoreCHK_query->rowcount()==7)
                                {
                                    
                                    $newRank=28/7;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==1 AND $scoreCHK_query->rowcount()==8)
                                {
                                    
                                    $newRank=36/8;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==1 AND $scoreCHK_query->rowcount()==9)
                                {
                                    
                                    $newRank=45/9;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==1 AND $scoreCHK_query->rowcount()==10)
                                {
                                    
                                    $newRank=55/10;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==1 AND $scoreCHK_query->rowcount()==11)
                                {
                                    
                                    $newRank=66/11;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==1 AND $scoreCHK_query->rowcount()==12)
                                {
                                    
                                    $newRank=78/12;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                               
                                
                                
                                
                                
                                //end of Tie ctr #1
                                
                                //start of Tie ctr #2
                                
                                
                                
                                elseif($rankCtr==2 AND $scoreCHK_query->rowcount()==2)
                                {
                                    
                                    $newRank=5/2;
                             
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                      
                                }
                                elseif($rankCtr==2 AND $scoreCHK_query->rowcount()==3)
                                {
                                    
                                    $newRank=9/3;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                  
                                }
                                elseif($rankCtr==2 AND $scoreCHK_query->rowcount()==4)
                                {
                                    
                                    $newRank=14/4;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==2 AND $scoreCHK_query->rowcount()==5)
                                {
                                    
                                    $newRank=20/5;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==2 AND $scoreCHK_query->rowcount()==6)
                                {
                                    
                                    $newRank=27/6;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==2 AND $scoreCHK_query->rowcount()==7)
                                {
                                    
                                    $newRank=35/7;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==2 AND $scoreCHK_query->rowcount()==8)
                                {
                                    
                                    $newRank=44/8;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==2 AND $scoreCHK_query->rowcount()==9)
                                {
                                    
                                    $newRank=54/9;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==2 AND $scoreCHK_query->rowcount()==10)
                                {
                                    
                                    $newRank=65/10;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==2 AND $scoreCHK_query->rowcount()==11)
                                {
                                    
                                    $newRank=77/11;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                 
                                
                   
                   
                                //end of Tie ctr #2
                                
                                //start of Tie ctr #3
                   
                   
                   
                                
                                elseif($rankCtr==3 AND $scoreCHK_query->rowcount()==2)
                                {
                                    
                                    $newRank=7/2;
                             
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                         
                                
                                }
                                elseif($rankCtr==3 AND $scoreCHK_query->rowcount()==3)
                                {
                                    
                                    $newRank=12/3;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                  
                                }
                                elseif($rankCtr==3 AND $scoreCHK_query->rowcount()==4)
                                {
                                    
                                    $newRank=18/4;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==3 AND $scoreCHK_query->rowcount()==5)
                                {
                                    
                                    $newRank=25/5;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==3 AND $scoreCHK_query->rowcount()==6)
                                {
                                    
                                    $newRank=33/6;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==3 AND $scoreCHK_query->rowcount()==7)
                                {
                                    
                                    $newRank=42/7;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==3 AND $scoreCHK_query->rowcount()==8)
                                {
                                    
                                    $newRank=52/8;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==3 AND $scoreCHK_query->rowcount()==9)
                                {
                                    
                                    $newRank=63/9;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==3 AND $scoreCHK_query->rowcount()==10)
                                {
                                    
                                    $newRank=75/10;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                               
                                
                                
                                //end of Tie ctr #3
                                
                                //start of Tie ctr #4
                                
                                
                                elseif($rankCtr==4 AND $scoreCHK_query->rowcount()==2)
                                {
                                    
                                    $newRank=9/2;
                             
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                           
                                
                                }
                                elseif($rankCtr==4 AND $scoreCHK_query->rowcount()==3)
                                {
                                    
                                    $newRank=15/3;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                  
                                }
                                elseif($rankCtr==4 AND $scoreCHK_query->rowcount()==4)
                                {
                                    
                                    $newRank=22/4;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==4 AND $scoreCHK_query->rowcount()==5)
                                {
                                    
                                    $newRank=30/5;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==4 AND $scoreCHK_query->rowcount()==6)
                                {
                                    
                                    $newRank=39/6;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==4 AND $scoreCHK_query->rowcount()==7)
                                {
                                    
                                    $newRank=49/7;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==4 AND $scoreCHK_query->rowcount()==8)
                                {
                                    
                                    $newRank=60/8;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==4 AND $scoreCHK_query->rowcount()==9)
                                {
                                    
                                    $newRank=72/9;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                               
         
                                 //end of Tie ctr #4
                                
                                //start of Tie ctr #5
                                
                                
                                elseif($rankCtr==5 AND $scoreCHK_query->rowcount()==2)
                                {
                                    
                                    $newRank=11/2;
                             
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                       
                                
                                }
                                elseif($rankCtr==5 AND $scoreCHK_query->rowcount()==3)
                                {
                                    
                                    $newRank=18/3;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                  
                                }
                                elseif($rankCtr==5 AND $scoreCHK_query->rowcount()==4)
                                {
                                    
                                    $newRank=26/4;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==5 AND $scoreCHK_query->rowcount()==5)
                                {
                                    
                                    $newRank=35/5;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==5 AND $scoreCHK_query->rowcount()==6)
                                {
                                    
                                    $newRank=45/6;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==5 AND $scoreCHK_query->rowcount()==7)
                                {
                                    
                                    $newRank=56/7;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==5 AND $scoreCHK_query->rowcount()==8)
                                {
                                    
                                    $newRank=68/8;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                
                             
         
                                 //end of Tie ctr #5
                                
                                //start of Tie ctr #6
                                
                                
                                elseif($rankCtr==6 AND $scoreCHK_query->rowcount()==2)
                                {
                                    
                                    $newRank=13/2;
                             
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                            
                                
                                }
                                elseif($rankCtr==6 AND $scoreCHK_query->rowcount()==3)
                                {
                                    
                                    $newRank=21/3;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                  
                                }
                                elseif($rankCtr==6 AND $scoreCHK_query->rowcount()==4)
                                {
                                    
                                    $newRank=30/4;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==6 AND $scoreCHK_query->rowcount()==5)
                                {
                                    
                                    $newRank=40/5;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==6 AND $scoreCHK_query->rowcount()==6)
                                {
                                    
                                    $newRank=51/6;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==6 AND $scoreCHK_query->rowcount()==7)
                                {
                                    
                                    $newRank=63/7;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                  
                  
                  
         
                                 //end of Tie ctr #6
                                
                                //start of Tie ctr #7
                                
                                elseif($rankCtr==7 AND $scoreCHK_query->rowcount()==2)
                                {
                                    
                                    $newRank=15/2;
                             
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                     
                                
                                }
                                elseif($rankCtr==7 AND $scoreCHK_query->rowcount()==3)
                                {
                                    
                                    $newRank=24/3;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                  
                                }
                                elseif($rankCtr==7 AND $scoreCHK_query->rowcount()==4)
                                {
                                    
                                    $newRank=34/4;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==7 AND $scoreCHK_query->rowcount()==5)
                                {
                                    
                                    $newRank=45/5;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==7 AND $scoreCHK_query->rowcount()==6)
                                {
                                    
                                    $newRank=57/6;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                     
                               
         
                                 //end of Tie ctr #7
                                
                                //start of Tie ctr #8
                                
                                
                                elseif($rankCtr==8 AND $scoreCHK_query->rowcount()==2)
                                {
                                    
                                    $newRank=17/2;
                             
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                    
                                
                                }
                                elseif($rankCtr==8 AND $scoreCHK_query->rowcount()==3)
                                {
                                    
                                    $newRank=27/3;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                  
                                }
                                elseif($rankCtr==8 AND $scoreCHK_query->rowcount()==4)
                                {
                                    
                                    $newRank=38/4;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                elseif($rankCtr==8 AND $scoreCHK_query->rowcount()==5)
                                {
                                    
                                    $newRank=50/5;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                               
                     
                                
         
                                 //end of Tie ctr #8
                                
                                //start of Tie ctr #9
                                
                                elseif($rankCtr==9 AND $scoreCHK_query->rowcount()==2)
                                {
                                    
                                    $newRank=19/2;
                             
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                     
                                
                                }
                                elseif($rankCtr==9 AND $scoreCHK_query->rowcount()==3)
                                {
                                    
                                    $newRank=30/3;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                  
                                }
                                elseif($rankCtr==9 AND $scoreCHK_query->rowcount()==4)
                                {
                                    
                                    $newRank=42/4;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                
                                }
                                
                       
                                
         
                                 //end of Tie ctr #9
                                
                                //start of Tie ctr #10
                                
                                elseif($rankCtr==10 AND $scoreCHK_query->rowcount()==2)
                                {
                                    
                                    $newRank=21/2;
                             
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                      
                                
                                }
                                elseif($rankCtr==10 AND $scoreCHK_query->rowcount()==3)
                                {
                                    
                                    $newRank=33/3;
                                  
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
                                  
                                }
                                 
                               
                                 //end of Tie ctr #10
                                
                                //start of Tie ctr #11
                                
                                
                                elseif($rankCtr==11 AND $scoreCHK_query->rowcount()==2)
                                {
                                    
                                    $newRank=23/2;
                             
                                    $conn->query("update sub_results set rank='$newRank', judge_rank_stat='tie' WHERE subevent_id='$subevent_id' AND total_score='$myScore' AND judge_id='$j_id'");
              
                                
                                }
                                 
                                else
                                
                                {
                                    
                                    $conn->query("update sub_results set rank='$rankCtr' WHERE subevent_id='$subevent_id' AND contestant_id='$conID' AND judge_id='$j_id' AND judge_rank_stat=''");
                                
                                } 
         
                                 //end of Tie ctr #11
                             
                        } 
                                ?>
<!-- auto ranking end --> <!-- auto ranking end --> <!-- auto ranking end --> <!-- auto ranking end --> <!-- auto ranking end --> <!-- auto ranking end --> <!-- auto ranking end --> <!-- auto ranking end --> 

                                
                        <td style="background:#e4f6e2">
                        
                        <center>
                        <br />
                        <br />
                        <font size="6"> <strong> <?php echo $myScore; ?> </strong> </font> 
                        </center>
                        
                        </td>
                        
                        
                        
                        <td bgcolor="green">
                        <center>
                        <br />
                        <br />
                        <font size="6" color="white">
                        <?php 
                        $rank_query = $conn->query("select * from sub_results where subevent_id='$subevent_id' and judge_id='$j_id' and contestant_id='$conID'") or die(mysql_error());
                        $rowRQ=$rank_query->fetch();
                        
                            echo $rowRQ['rank'];
                            
                         ?>
                         </font>
                        </center>
                        
                         </td> 
                         
                         
                         
                        <td width="10">
                        <br />
                        <br />
                        <a title="Change <?php echo $contzx_row['fullname']; ?> scores" href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=<?php echo $conID;?>" class="btn btn-success"><i class="icon-pencil"></i></a>
                        </td>
                        
                        </tr>
                         
                         
                            
                        <?php } ?>
                        
                        <tr>
                        <td colspan="5">
                        
                        <center>
                        <p><strong class="aleret alert-danger">In case of tie, please break the tie by clicking the change button and change the scores.</strong></p>
                        </center>
                        </td>
                        </tr>
                        
                        </table>
                

                
 
                <a href="#" title="Back to Top" class="btn btn-default pull-right"><i class="icon-chevron-up"></i></a>
                 
                <footer class="footer">
                
                 
                 <?php   
                 
                     if($pageStat=="Change")
                     {
                    $cont_query = $conn->query("select * from contestants where subevent_id='$subevent_id' AND contestant_id='$getContestant_id'") or die(mysql_error());
                    while ($cont_row = $cont_query->fetch()) { 
                    $con_idTab=$cont_row['contestant_id'];
                    ?>
                     <strong>Edit Score Mode :</strong> <?php echo $cont_row['fullname']; ?>
                     <?php }
                     
                     
                     } else {
                        
                    $cont_query = $conn->query("select * from contestants where subevent_id='$subevent_id' order by contestant_ctr") or die(mysql_error());
                    while ($cont_row = $cont_query->fetch()) { 
                    $con_idTab=$cont_row['contestant_id'];
                    
                    ?>
                    <?php if($getContestant_id==$con_idTab){?>
                       <strong><a href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=<?php echo $con_idTab;?>"><?php echo $cont_row['fullname']; ?></a></strong> &middot;
                    <?php }else{?> 
                   <a href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=<?php echo $con_idTab;?>"><?php echo $cont_row['fullname']; ?></a> &middot;
                    <?php } } ?>
                    <?php if($getContestant_id=="allTally"){?>
                   <strong><a href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=allTally">View Tally</a></strong>  
                   <a> &middot; </a><a href="selection.php"><strong><font color="red">Exit</font></strong></a>
                    <?php }else{?>
                   <a href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=allTally">View Tally</a>  
                     <?php  } 
                     
                     }?>
                 
                                        <div class="container">
                                          <center>
                                          
                                          <font size="4">Judging Management System &middot; &COPY; <?= date ("Y") ?></font>
                                          <hr />
                                          
                                          
                                          <table border="0">
      
                                          <tr>
                                          <td align="center"><img src="uploads/<?php echo $company_logo; ?>" width="35" height="35" /></td>
                                         </tr>
                                         <tr>
                                          <td align="center">
                                           
                                          <font size="3"><?php echo $company_name; ?></font>
                                          </td>
                                          </tr>
                                          <tr>
                                          <td align="center">
                                            <font size="2"><?php echo $company_address; ?></font> <br />
                                     
                                            <font size="2">Tel. No.: <?php echo $company_telephone; ?><br />
                                            Email Address: <?php echo $company_email; ?><br />
                                            Website: <a href="<?php echo $company_website; ?>" target="_blank"><?php echo $company_website; ?></a></font>
                                          
                                          </td>
                                          </tr>
                                      
                                          </table>
                                          
                                          </center>
                                          
                                          </div>
                 
                  </footer>

                
<!-- end all tally -->
 
 
 
 
 
 <!-- update --> <!-- update --> <!-- update --> <!-- update --> <!-- update --> <!-- update --> <!-- update -->
 
<?php }else{ 


$cont_query = $conn->query("select * from contestants where subevent_id='$subevent_id' AND contestant_id='$getContestant_id'") or die(mysql_error());
while ($cont_row = $cont_query->fetch()) { 
 
    
    $score_query = $conn->query("select * from sub_results where contestant_id='$getContestant_id' AND judge_id='$j_id'") or die(mysql_error());
while ($score_row = $score_query->fetch())
 {
     $s1=$score_row['criteria_ctr1'];
     $s2=$score_row['criteria_ctr2'];
     $s3=$score_row['criteria_ctr3'];
     $s4=$score_row['criteria_ctr4'];
     $s5=$score_row['criteria_ctr5'];
     $s6=$score_row['criteria_ctr6'];
     $s7=$score_row['criteria_ctr7'];
     $s8=$score_row['criteria_ctr8'];
     $s9=$score_row['criteria_ctr9'];
     $s10=$score_row['criteria_ctr10'];
     $comments=$score_row['comments'];
 }
    
    ?>
<table align="center" style="width: 100% !important;">
<tr>
<td align="center">

<h3><?php echo $se_namexx; ?> - <?php echo $cont_row['fullname']; ?></h3>
 
Total Score Earned:
<strong><?php $score_query = $conn->query("select * from sub_results where subevent_id='$subevent_id' and judge_id='$j_id' and contestant_id='$getContestant_id'") or die(mysql_error());
while ($score_row = $score_query->fetch()) { echo $score_row['total_score']."%"; }?> of 100% </strong>
 
<br />
<br />
       
<?php 
$jstat_rowx=0;

$jstat_query = $conn->query("select * from sub_results where subevent_id='$subevent_id' and judge_id='$j_id' and contestant_id='$getContestant_id'") or die(mysql_error());
while ($jstat_row = $jstat_query->fetch()) 
{
   $jstat_rowx=1; 
   
}

if( $jstat_rowx == 1 ) 
{ ?>



<form method="POST" action="edit_submit_judging.php">

                  <input type="hidden" value="<?php echo $cont_row['fullname']; ?>" name="contestant_name" />
                  <input type="hidden" value="<?php echo $getContestant_id; ?>" name="contestant_id" />
                  <input type="hidden" value="<?php echo $j_id; ?>" name="judge_id" />
                  <input type="hidden" value="<?php echo $judge_ctr; ?>" name="judge_ctr" />
                  <input type="hidden" value="<?php echo $se_MEidxx; ?>" name="mainevent_id" />
                  <input type="hidden" value="<?php echo $subevent_id; ?>" name="subevent_id" />
 
                <table align="center" class="table table-bordered">
                
                <tr>
                <?php
                 
                $totzxzxzxzxz=0;
                
                $criteria_query = $conn->query("select * from criteria where subevent_id='$subevent_id' order by criteria_ctr ASC") or die(mysql_error());
                while ($crit_row = $criteria_query->fetch()) { $totzxzxzxzxz=$crit_row['percentage']+$totzxzxzxzxz; }  
                
                $criteria_query = $conn->query("select * from criteria where subevent_id='$subevent_id' order by criteria_ctr ASC") or die(mysql_error());
                while ($crit_row = $criteria_query->fetch()) { ?>
                
                <td width="10"><center><font size="2"><?php echo $crit_row['criteria']." - <b>".$crit_row['percentage']."%</b>";?></font></center></td>
                 
                <?php } ?>
                </tr>
                 
                <tr>
                <?php   
                
                $totzxzxzxzxz=0;
                
                $criteria_query = $conn->query("select * from criteria where subevent_id='$subevent_id' order by criteria_ctr ASC") or die(mysql_error());
                while ($crit_row = $criteria_query->fetch()) { $totzxzxzxzxz=$crit_row['percentage']+$totzxzxzxzxz; }  
                
                $criteria_query = $conn->query("select * from criteria where subevent_id='$subevent_id' order by criteria_ctr ASC") or die(mysql_error());
                while ($crit_row = $criteria_query->fetch()) { ?>
                 
                <td width="10">
                 
                <?php if($pageStat=="Change") { ?>
                <center>
                <select class="form-control" style="width: 100%;" name="cp<?php echo $crit_row['criteria_ctr']; ?>">
                </center>
                <?php }else{ ?>
                <center>
                <select class="form-control" style="width: 100%;" name="cp<?php echo $crit_row['criteria_ctr']; ?>" disabled="true">
                </center>
                <?php } 
                
                if($crit_row['criteria_ctr']==1) { ?>
                
                <option><?php echo $s1; ?></option>
                <?php }
                
                if($crit_row['criteria_ctr']==2){ ?>
                
                <option><?php echo $s2; ?></option>
                
                <?php }
                
                if($crit_row['criteria_ctr']==3){ ?>
                
                <option><?php echo $s3; ?></option>
                
                <?php }
                
                if($crit_row['criteria_ctr']==4){ ?>
                
                <option><?php echo $s4; ?></option>
                
                <?php }
                
                if($crit_row['criteria_ctr']==5){ ?>
                
                <option><?php echo $s5; ?></option>
                
                <?php } 
                
                if($crit_row['criteria_ctr']==6){ ?>
                 
                <option><?php echo $s6; ?></option>
                
                <?php }
                
                if($crit_row['criteria_ctr']==7) { ?>
                
                <option><?php echo $s7; ?></option>
                
                <?php } 
                
                if($crit_row['criteria_ctr']==8){ ?>
                
                <option><?php echo $s8; ?></option>
                
                <?php }
                
                if($crit_row['criteria_ctr']==9){ ?>
                
                <option><?php echo $s9; ?></option>
                
                <?php }
                
                if($crit_row['criteria_ctr']==10)
                { ?>
                     <option><?php echo $s10; ?></option>
                     
                <?php }
                
                $n1=-0.5;
                while($n1<$crit_row['percentage'])
                { $n1=$n1+0.5;
                
                ?>
                <option><?php echo $n1; ?></option>
                <?php } ?>
                
                </select>
                
                </td>
                
                <?php } ?>
                
                </tr>
                 
                </table>
                
                <tr>
                <td>
                <?php if($pageStat=="Change") { ?>
                <strong>COMMENTS:</strong><br />
                <textarea name="jcomment" class="form-control" style="width: 99%;" placeholder="Enter comments here..."><?php echo $comments; ?></textarea>
                <?php }else{ ?>
                <strong>COMMENTS:</strong><br />
                <textarea readonly="true" name="jcomment" class="form-control" style="width: 99%;" placeholder="Enter comments here..."><?php echo $comments; ?></textarea>
                <?php } ?>
                </td>
                </tr>
                
                
</td>
</tr>
</table>
 
                <div class="modal-footer">
                <?php if($totzxzxzxzxz>100 or $totzxzxzxzxz<100) {  if($totzxzxzxzxz>100) { ?>
                <div class="alert alert-danger pull-right">
                  
                <strong>The Total Percentage is over 100%. Pls. contact event organizer.</strong> 
                </div> 
                <?php } if($totzxzxzxzxz<100) { ?>
                <div class="alert alert-danger pull-right">
                  
                <strong>The Total Percentage is under 100%. Pls. contact event organizer.</strong> 
                </div>  
                <?php } } else {  if($pageStat=="Change") { ?>
                           
                <a title="click to cancel, changes made will never be save." href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=<?php echo $getContestant_id; ?>&pStat=xChange" class="btn btn-default"><i class="icon-remove"></i> <strong>CANCEL</strong></a>
                <button title="Click to update scores." type="submit" class="btn btn-success"><i class="icon-ok"></i> <strong>UPDATE</strong></button>
                <?php }else{ ?>
                <a href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=<?php echo $getContestant_id; ?>&pStat=Change" class="btn btn-default"><i class="icon-pencil"></i> <strong>CHANGE</strong></a>
                <?php } } ?>
                          
                </div>
      
</form>
 


<!-- end update --><!-- end update --><!-- end update --><!-- end update --><!-- end update --><!-- end update -->



 


<?php }else{ ?>
   
 
 
 
   

<!-- submit -->  <!-- submit -->  <!-- submit -->  <!-- submit -->  <!-- submit -->  <!-- submit -->  <!-- submit -->
 
      <form method="POST" action="submit_judging.php">
      
                  <input type="hidden" value="<?php echo $cont_row['fullname']; ?>" name="contestant_name" />
                  <input type="hidden" value="<?php echo $getContestant_id; ?>" name="contestant_id" />
                  <input type="hidden" value="<?php echo $j_id; ?>" name="judge_id" />
                  <input type="hidden" value="<?php echo $judge_ctr; ?>" name="judge_ctr" />
                  <input type="hidden" value="<?php echo $se_MEidxx; ?>" name="mainevent_id" />
                  <input type="hidden" value="<?php echo $subevent_id; ?>" name="subevent_id" />
 
            
<table align="center" style="width: 100%;">
<tr>
<td>

                    <table align="center" class="table table-bordered">
                 
                    <tr>
                    <?php   
                
                    $totzxzxzxzxz=0;
                    
                    $criteria_query = $conn->query("select * from criteria where subevent_id='$subevent_id' order by criteria_ctr ASC") or die(mysql_error());
                    while ($crit_row = $criteria_query->fetch()) { 
                    
                    $totzxzxzxzxz=$crit_row['percentage']+$totzxzxzxzxz;
                    
                    ?>
                 
                    <td width="10"><center><font size="2"><?php echo $crit_row['criteria']." - <b>".$crit_row['percentage']."%</b>";?></font></center></td>
                 
                    <?php } ?>
                    </tr>
                
                 
                    <tr>
                    <?php   
                    
                    $totzxzxzxzxz=0;
                    
                    $criteria_query = $conn->query("select * from criteria where subevent_id='$subevent_id' order by criteria_ctr ASC") or die(mysql_error());
                    while ($crit_row = $criteria_query->fetch()) { 
                    
                    $totzxzxzxzxz=$crit_row['percentage']+$totzxzxzxzxz;
                    
                    ?>
                    
                    
                     
                    <td><select class="form-control" style="width: 100%;" name="cp<?php echo $crit_row['criteria_ctr']; ?>">
                    <?php $n1=-0.5;
                    while($n1<$crit_row['percentage'])
                    { $n1=$n1+0.5; ?>
                      
                    <option><?php echo $n1; ?></option>
                      
                    <?php } ?>
                    </select></td>
                    
                    <?php } ?>
                    </tr>
       
                </table>
                
                <tr>
                <td>
                <strong>COMMENTS:</strong><br />
                <textarea name="jcomment" class="form-control" style="width: 99%;" placeholder="Enter comments here..."></textarea>
                </td>
                </tr>
                
</td>
</tr>
</table>


   
     
      
                  <div class="modal-footer">
                   
                       <?php if($totzxzxzxzxz>100 or $totzxzxzxzxz<100)
                    { 
                        if($totzxzxzxzxz>100)
                        { ?>
                        <div class="alert alert-danger pull-right">
                        <strong>The Total Percentage is over 100%. Pls. contact event organizer.</strong> 
                        </div> 
                       <?php }
                        
                        if($totzxzxzxzxz<100)
                        { ?>
                        <div class="alert alert-danger pull-right">
                        <strong>The Total Percentage is under 100%. Pls. contact event organizer.</strong> 
                        </div>  
                       <?php } } else { ?>
                       <button type="submit" class="btn btn-primary"><i class="icon-ok"></i> <strong>SUBMIT</strong></button>  
                  <?php  } ?>
                     
                  </div>
      
      </form>
       
<!-- END submit --><!-- END submit --><!-- END submit --><!-- END submit --><!-- END submit --><!-- END submit -->
      
<?php }  } ?>
 

 
 
 
 
</div> </div> </div>

                       
                        
<div class="footer">

 
 <?php   
 
 if($pageStat=="Change")
 {
    $cont_query = $conn->query("select * from contestants where subevent_id='$subevent_id' AND contestant_id='$getContestant_id'") or die(mysql_error());
    while ($cont_row = $cont_query->fetch()) { 
    $con_idTab=$cont_row['contestant_id'];
    ?>
     <strong>Edit Score Mode :</strong> <?php echo $cont_row['fullname']; ?>
     <?php }
     
     
     } else {
        
    $cont_query = $conn->query("select * from contestants where subevent_id='$subevent_id' order by contestant_ctr") or die(mysql_error());
    while ($cont_row = $cont_query->fetch()) { 
    $con_idTab=$cont_row['contestant_id'];
    
    ?>
    <?php if($getContestant_id==$con_idTab){?>
       <strong><a href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=<?php echo $con_idTab;?>"><?php echo $cont_row['fullname']; ?></a></strong> &middot;
    <?php }else{?> 
   <a href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=<?php echo $con_idTab;?>"><?php echo $cont_row['fullname']; ?></a> &middot;
    <?php } } ?>
    <?php if($getContestant_id=="allTally"){?>
   <strong><a href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=allTally">View Tally</a></strong>  
    <a href="selection.php"><strong><font color="red">Exit</font></strong></a>
    <?php }else{?>
   <a href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=allTally">View Tally</a>  
     <?php  } 
     
     }?>
     
     
     
      
      
     
                          <div class="container">
                          <center>
                          
                          <?php include('footer.php'); ?>
                          
                          </center>
                          
                          </div>
 
</div>
     
 
     
<?php } } else{ ?> 

<hr />
<a class="btn btn-danger btn-block" href="selection.php">Back to Selection Panel</a>


<?php include('footer.php'); ?>


<?php } ?> 

 
 
 
  
    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script type="text/javascript" src="http://platform.twitter.com/widgets.js"></script>
    <script src="assets/js/jquery.js"></script>
    <script src="assets/js/bootstrap-transition.js"></script>
    <script src="assets/js/bootstrap-alert.js"></script>
    <script src="assets/js/bootstrap-modal.js"></script>
    <script src="assets/js/bootstrap-dropdown.js"></script>
    <script src="assets/js/bootstrap-scrollspy.js"></script>
    <script src="assets/js/bootstrap-tab.js"></script>
    <script src="assets/js/bootstrap-tooltip.js"></script>
    <script src="assets/js/bootstrap-popover.js"></script>
    <script src="assets/js/bootstrap-button.js"></script>
    <script src="assets/js/bootstrap-collapse.js"></script>
    <script src="assets/js/bootstrap-carousel.js"></script>
    <script src="assets/js/bootstrap-typeahead.js"></script>
    <script src="assets/js/bootstrap-affix.js"></script>

    <script src="assets/js/holder/holder.js"></script>
    <script src="assets/js/google-code-prettify/prettify.js"></script>

    <script src="assets/js/application.js"></script>
  
  </body>
</html>
 




