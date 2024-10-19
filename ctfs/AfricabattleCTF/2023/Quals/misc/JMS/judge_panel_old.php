 
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
<table style="background-color: #44BA2B; width: 100% !important; height: 150px; text-indent: 25px;" align="center" border="0">
<tr>
<td>
<h1 style="color: whitesmoke !important;">Judge's Panel</h1>
<h4 style="color: whitesmoke !important;">Judging Management System</h4>
</td>
</tr>
</table>
 


         <br />
        <?php } } } else { $j_name="Event is still inactive. Please contact the Event Organizer."; ?>


<table style="background-color: #44BA2B; width: 100% !important; height: 150px; text-indent: 25px;" align="center" border="0">
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



  <div class="container"> <div class="row"> <div class="span12">
 
  
        
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
                        <td bgcolor="yellow"><center>Final Score</center></td>
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
                        
                        
                          
                            
                        <?php
                           
                        $score_query = $conn->query("select * from sub_results where subevent_id='$subevent_id' and judge_id='$j_id' and contestant_id='$conID'") or die(mysql_error());
                        while ($score_row = $score_query->fetch()) 
                        { 
                            
                                $myScore=$score_row['total_score'];
                                     
                                $scoreCHK_query = $conn->query("select * from sub_results where subevent_id='$subevent_id' and judge_id='$j_id' and total_score='$myScore'") or die(mysql_error());
                                    
                                if($rankCtr==1 AND $scoreCHK_query->rowcount()==2)
                                {
                                  $newRank=3/2;
                                }
                                
                                if($rankCtr==1 AND $scoreCHK_query->rowcount()==2)
                                {
                                  $newRank=3/2;
                                }
                                
                                
                      
                                
                        }
                            ?>
                       
                       
                        <td bgcolor="yellow" align="center"><font size="6"> <strong> <?php echo $myScore; ?> </strong> </font> </td>
                      
                        <td bgcolor="green" align="center"><font size="6" color="white"><?php echo $rankCtr; ?></font></td>  
                        <td width="10" align="center"><a title="Change <?php echo $contzx_row['fullname']; ?> scores" href="judge_panel.php?judge_ctr=<?php echo $judge_ctr; ?>&subevent_id=<?php echo $subevent_id; ?>&contestant_id=<?php echo $conID;?>" class="btn btn-success"><i class="icon-pencil"></i></a></td>
                        
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
                                          <td rowspan="3" width="10"><img src="uploads/<?php echo $company_logo; ?>" width="35" height="35" /> <br /><br /><br /> <br /> <br /> <br /></td>
                                         </tr>
                                         <tr>
                                          <td align="center">
                                           
                                          <font size="3"><?php echo $company_name; ?></font>
                                          </td>
                                          </tr>
                                          <tr>
                                          <td colspan="2" align="center">
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
 




