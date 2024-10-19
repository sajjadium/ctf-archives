<!DOCTYPE html>
<html lang="en">

<?php 
  include('header2.php');
    include('session.php');
    
    
    $sub_event_id=$_GET['sub_event_id'];
    $se_name=$_GET['se_name'];
    
    
$se_query = $conn->query("select * from sub_event where subevent_id = '$sub_event_id'");
$se_row = $se_query->fetch();
     
  ?>



<body data-spy="scroll" data-target=".bs-docs-sidebar">

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
        <a class="brand" href="#"><img src="uploads/<?php echo $company_logo; ?>" width="23" height="23" />&nbsp; <font
            size="3">Judging Management System</font></a>
        <div class="nav-collapse collapse">
          <ul class="nav">

            <li>
              <a href="selection.php">User Selection</a>
            </li>

            <li class="active">
              <a href="home.php"><strong>LIST OF EVENTS</strong></a>
            </li>

            <li>
              <a href="score_sheets.php">Score Sheets</a>
            </li>


            <li>
              <a href="rev_main_event.php">Data Reviews</a>
            </li>




            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">My Account
                <span class="caret"></span></a>
              <ul class="dropdown-menu" role="menu">


                <li>
                  <a target="_blank" href="edit_organizer.php">Settings</a>
                </li>

                <li>
                  <a href="logout.php">Logout
                    <?php echo $name; ?>
                  </a>
                </li>


              </ul>
            </li>

          </ul>
        </div>
      </div>
    </div>
  </div>


  <header class="jumbotron subhead" id="overview">
    <div class="container">
      <h1>
        <?php echo $se_name; ?> Settings
      </h1>
      <p class="lead">Judging Management System</p>
    </div>
  </header>


  <div class="container">






    <div class="span12">



      <br />
      <div class="col-md-12">
        <ul class="breadcrumb">

          <li><a href="selection.php">User Selection</a> / </li>

          <li><a href="home.php">List of Events</a> / </li>

          <li>
            <?php echo $se_name; ?> Settings
          </li>

        </ul>
      </div>




      <form method="POST">
        <input value="<?php echo $sub_event_id; ?>" name="sub_event_id" type="hidden" />


        <hr />

        <div id="myGroup">


          <a class="btn btn-info" style="margin-bottom: 4px !important;" data-toggle="collapse"
            data-target="#contestant" data-parent="#myGroup"><i class="icon-chevron-right"></i>
            <strong>CONTESTANT</strong></a>

          <a class="btn btn-info" style="margin-bottom: 4px !important;" data-toggle="collapse" data-target="#judges"
            data-parent="#myGroup"><i class="icon-chevron-right"></i> <strong>JUDGE</strong></a>

          <a class="btn btn-info" style="margin-bottom: 4px !important;" data-toggle="collapse" data-target="#criteria"
            data-parent="#myGroup"><i class="icon-chevron-right"></i> <strong>CRITERIA</strong></a>



          <div style="border: 0px;" class="accordion-group">

            <div class="collapse indent" id="contestant">


              <section id="download-bootstrap">
                <div class="page-header">
                  <h1>Contestant's Settings
                    &nbsp;<a title="Click to add new Contestant for this Event"
                      href="add_contestant.php?sub_event_id=<?php echo $sub_event_id; ?>&se_name=<?php echo $se_name;?>"
                      class="btn btn-primary"><i class="icon icon-plus"></i></a>
                  </h1>
                </div>

                <table class="table table-bordered">

                  <thead>
                    <th>Check to Select</th>
                    <th>No.</th>
                    <th>Name</th>
                    <th>Actions</th>
                  </thead>
                  <form method="POST">

                    <tbody>
                      <?php    
                                       	$cont_query = $conn->query("SELECT * FROM contestants WHERE subevent_id='$sub_event_id' order by contestant_ctr") or die(mysql_error());
                                        while ($cont_row = $cont_query->fetch()) 
                                            { 
                                                $cont_id=$cont_row['contestant_id'];
                                                ?>

                      <tr>

                        <td width="115">

                          <input name="selector[]" type="checkbox" value="<?php echo $cont_id; ?>"
                            title="Check to select <?php echo $cont_row['fullname']; ?>" />
                        </td>

                        <td width="10">
                          <?php echo $cont_row['contestant_ctr']; ?>
                        </td>
                        <td>
                          <?php echo $cont_row['fullname']; ?>
                        </td>
                        <td width="10"><a title="Click to edit <?php echo $cont_row['fullname']; ?> datas"
                            href="edit_contestant.php?contestant_id=<?php echo $cont_row['contestant_id'];?>&sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>"
                            class="btn btn-success"><i class="icon icon-pencil"></i></a></td>
                      </tr>
                      <?php } ?>
                      <tr>

                        <td colspan="4">
                          <input required="true" type="password" placeholder="Organizer Password" name="org_pass" />
                          <input type="hidden" name="sub_event_id" value="<?php echo $sub_event_id; ?>" />
                          <input type="hidden" name="se_name" value="<?php echo $se_name; ?>" />

                          <button title="Click to delete selected row(s)" type="submit" class="btn btn-danger"
                            name="delete_cont"><i class="icon icon-trash"></i></button>

                        </td>
                      </tr>

                    </tbody>

                  </form>

                </table>

              </section>

            </div>









            <div class="collapse indent" id="judges">
              <section id="download-bootstrap">
                <div class="page-header">
                  <h1>Judge's Settings
                    &nbsp;<a title="Click to add new Judge for this Event"
                      href="add_judge.php?sub_event_id=<?php echo $sub_event_id; ?>&se_name=<?php echo $se_name;?>"
                      class="btn btn-primary"><i class="icon icon-plus"></i></a>
                    &nbsp;<a title="Click to print Judge's Code for this Event" target="_blank"
                      title="Click to print judges code"
                      href="print_judges.php?sub_event_id=<?php echo $sub_event_id; ?>&se_name=<?php echo $se_name;?>"
                      class="btn btn-info"><i class="icon icon-print"></i></a></h1>
                </div>
                <table class="table table-bordered">
                  <thead>
                    <th>Check to Select</th>
                    <th>No.</th>
                    <th>Code</th>
                    <th>Fullname</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </thead>
                  <form method="POST">
                    <tbody>
                      <?php    
   	$judge_query = $conn->query("SELECT * FROM judges WHERE subevent_id='$sub_event_id' order by judge_ctr") or die(mysql_error());
    while ($judge_row = $judge_query->fetch()) 
        { 
            $jxx_id=$judge_row['judge_id'];
            ?>
                      <tr>
                        <td width="115"><input name="selector[]" type="checkbox" value="<?php echo $jxx_id;  ?>"
                            title="Check to select <?php echo $judge_row['fullname']; ?>" /></td>
                        <td width="10">
                          <?php echo $judge_row['judge_ctr']; ?>
                        </td>
                        <td>
                          <?php echo $judge_row['code']; ?>
                        </td>
                        <td>
                          <?php echo $judge_row['fullname']; ?>
                        </td>
                        <td>
                          <?php echo $judge_row['jtype']; ?>
                        </td>
                        <td width="10"><a title="Click to edit <?php echo $judge_row['fullname']; ?> datas"
                            href="edit_judge.php?judge_id=<?php echo $jxx_id;?>&sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>"
                            class="btn btn-success"><i class="icon icon-pencil"></i></a>


                        </td>
                      </tr>





                      <?php } ?>
                      <tr>
                        <td colspan="6">
                          <input required="true" type="password" placeholder="Organizer Password" name="org_pass" />
                          <input type="hidden" name="sub_event_id" value="<?php echo $sub_event_id; ?>" />
                          <input type="hidden" name="se_name" value="<?php echo $se_name; ?>" />

                          <button title="Click to delete selected row(s)" type="submit" class="btn btn-danger"
                            name="delete_judge"><i class="icon icon-trash"></i></button>
                        </td>
                      </tr>
                </table>
                </td>

                </tr>
                </tbody>
      </form>
      </table>




      </section>
    </div>





    <div class="collapse indent" id="criteria">
      <section id="download-bootstrap">
        <div class="page-header">
          <h1>Criteria's Settings &nbsp;<a title="Click to add new Criteria for this Event"
              href="add_criteria.php?sub_event_id=<?php echo $sub_event_id; ?>&se_name=<?php echo $se_name;?>"
              class="btn btn-primary"><i class="icon icon-plus"></i></a></h1>
        </div>
        <table class="table table-bordered">
          <thead>
            <th>Check to Select</th>
            <th>No.</th>
            <th>Criteria</th>
            <th>Percentage</th>
            <th>Actions</th>
          </thead>
          <form method="POST">
            <tbody>
              <?php    
  $percnt=0;
   	$crit_query = $conn->query("SELECT * FROM criteria WHERE subevent_id='$sub_event_id'") or die(mysql_error());
    while ($crit_row = $crit_query->fetch()) 
        { $percnt=$percnt+$crit_row['percentage'];
            $crit_id=$crit_row['criteria_id'];
            ?>
              <tr>
                <td width="115"><input name="selector[]" type="checkbox" value="<?php echo $crit_id; ?>"
                    title="Check to select <?php echo $crit_row['criteria']; ?>" /></td>
                <td width="10">
                  <?php echo $crit_row['criteria_ctr']; ?>
                </td>
                <td>
                  <?php echo $crit_row['criteria']; ?>
                </td>
                <td width="10">
                  <?php echo $crit_row['percentage']; ?>
                </td>
                <td width="10"><a title="Click to edit Criteria: <?php echo $crit_row['criteria']; ?> datas"
                    href="edit_criteria.php?crit_id=<?php echo $crit_id;?>&sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>"
                    class="btn btn-success"><i class="icon icon-pencil"></i></a></td>
              </tr>
              <?php } ?>

              <tr>

                <?php
      if($percnt<100)
      { ?>
                <td colspan="3">
                  <div class="alert alert-danger pull-right">

                    <strong>The Total Percentage is under 100%.</strong>
                  </div>
                </td>
                <td colspan="2">
                  <div class="alert alert-danger">

                    <strong>
                      <?php  echo $percnt; ?>%
                    </strong>
                  </div>
                </td>

                <?php } ?>

                <?php
      if($percnt>100)
      { ?>
                <td colspan="3">
                  <div class="alert alert-danger pull-right">

                    <strong>The Total Percentage is over 100%.</strong>
                  </div>
                </td>
                <td colspan="2">
                  <div class="alert alert-danger">

                    <strong>
                      <?php  echo $percnt; ?>%
                    </strong>
                  </div>

                </td>

                <?php } ?>


                <?php
      if($percnt==100)
      { ?>
                <td colspan="3"><strong class="pull-right">TOTAL</strong></td>
                <td colspan="2">
                  <span style="font-size: 15px !important;" class="badge badge-info">
                    <?php  echo $percnt; ?> %
                  </span>
                </td>

                <?php } ?>
              </tr>


              <tr>
                <td colspan="5">
                  <input required="true" type="password" placeholder="Organizer Password" name="org_pass" />
                  <input type="hidden" name="sub_event_id" value="<?php echo $sub_event_id; ?>" />
                  <input type="hidden" name="se_name" value="<?php echo $se_name; ?>" />
                  <button title="Click to delete selected row(s)" type="submit" class="btn btn-danger"
                    name="delete_crit"><i class="icon icon-trash"></i></button>
                </td>
              </tr>
            </tbody>
          </form>
        </table>

      </section>
    </div>


  </div>



  </div>



  </form>
  </div>
  </div>

  <?php
 if (isset($_POST['activate_textpoll']))
{

$sub_event_id=$_POST['sub_event_id'];
$tp_status=$_POST['tp_status'];
 
 if($tp_status=="active")
 {
 $conn->query("update sub_event set txtpoll_status='deactive', txtpollview='deactive', view='deactive' where subevent_id='$sub_event_id'");  
 
 ?>
  <script>window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
    alert('Textpoll Deactivated');</script>
  <?php 
 }
    
 else
 
 {
 $conn->query("update sub_event set txtpoll_status='active', txtpollview='active', view='active' where subevent_id='$sub_event_id'");  
 
 ?>
  <script>window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
    alert('Textpoll Activated');</script>

  <?php  }}?>



  <?php 

if(isset($_POST['save_settings']))
{
    
    
    $sub_event_id=$_POST['sub_event_id'];
    
 /* contestants */
 
   $con1_name=$_POST['con1'];
   if($con1_name=="")
   {
    
   }
   else
   {
     $conn->query("insert into contestants(fullname,subevent_id,contestant_ctr)values('$con1_name','$sub_event_id','1')");
   }
  
   
   $con2_name=$_POST['con2'];
   if($con2_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into contestants(fullname,subevent_id,contestant_ctr)values('$con2_name','$sub_event_id','2')");
   }
   
   
   $con3_name=$_POST['con3'];
   if($con3_name=="")
   {
    
   }
   else
   {
     $conn->query("insert into contestants(fullname,subevent_id,contestant_ctr)values('$con3_name','$sub_event_id','3')");
   }
  
   
   $con4_name=$_POST['con4'];
   if($con4_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into contestants(fullname,subevent_id,contestant_ctr)values('$con4_name','$sub_event_id','4')");
   }
   
   
   $con5_name=$_POST['con5'];
   if($con5_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into contestants(fullname,subevent_id,contestant_ctr)values('$con5_name','$sub_event_id','5')");
   }
   
   
   $con6_name=$_POST['con6'];
   if($con6_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into contestants(fullname,subevent_id,contestant_ctr)values('$con6_name','$sub_event_id','6')");
   }
   
   
   $con7_name=$_POST['con7'];
   if($con7_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into contestants(fullname,subevent_id,contestant_ctr)values('$con7_name','$sub_event_id','7')");
   }
   
   
   $con8_name=$_POST['con8'];
   if($con8_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into contestants(fullname,subevent_id,contestant_ctr)values('$con8_name','$sub_event_id','8')");
   }
   
   
   $con9_name=$_POST['con9'];
   if($con9_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into contestants(fullname,subevent_id,contestant_ctr)values('$con9_name','$sub_event_id','9')");
   }
   
   
   $con10_name=$_POST['con10'];
   if($con10_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into contestants(fullname,subevent_id,contestant_ctr)values('$con10_name','$sub_event_id','10')");
   }
   
 /* end contestants */
   
   
   
   /* judges */
    $j1_name=$_POST['jud1'];
   if($j1_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into judges(fullname,subevent_id,judge_ctr)values('$j1_name','$sub_event_id','1')");
   }
   
   
   $j2_name=$_POST['jud2'];
   if($j2_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into judges(fullname,subevent_id,judge_ctr)values('$j2_name','$sub_event_id','2')");
   }
   
   
   $j3_name=$_POST['jud3'];
   if($j3_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into judges(fullname,subevent_id,judge_ctr)values('$j3_name','$sub_event_id','3')");
   }
   
   
   $j4_name=$_POST['jud4'];
   if($j4_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into judges(fullname,subevent_id,judge_ctr)values('$j4_name','$sub_event_id','4')");
   }
   
   
   $j5_name=$_POST['jud5'];
   if($j5_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into judges(fullname,subevent_id,judge_ctr)values('$j5_name','$sub_event_id','5')");
   }
   
   
   $j6_name=$_POST['j6'];
   if($j6_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into judges(fullname,subevent_id,judge_ctr)values('$j6_name','$sub_event_id','6')");
   }
   
   
   $j7_name=$_POST['j7'];
   if($j7_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into judges(fullname,subevent_id,judge_ctr)values('$j7_name','$sub_event_id','7')");
   }
   
   
   $j8_name=$_POST['j8'];
   if($j8_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into judges(fullname,subevent_id,judge_ctr)values('$j8_name','$sub_event_id','8')");
   }
   
   
   $j9_name=$_POST['j9'];
   if($j9_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into judges(fullname,subevent_id,judge_ctr)values('$j9_name','$sub_event_id','9')");
   }
   
   
   $j10_name=$_POST['j10'];
   if($j10_name=="")
   {
    
   }
   else
   {
    $conn->query("insert into judges(fullname,subevent_id,judge_ctr)values('$j10_name','$sub_event_id','10')");
   }
 /* judges */
 
 
 
  /* criteria */
   $c1_name=$_POST['crit1']; 
    $cp1=$_POST['cp1'];
  if($c1_name!="" or $cp1>0)
    {
      $conn->query("insert into criteria(criteria,subevent_id,percentage,criteria_ctr)values('$c1_name','$sub_event_id','$cp1','1')"); 
    }
    
    
       $c2_name=$_POST['crit2']; 
    $cp2=$_POST['cp2'];
   if($c2_name!="" or $cp1>0)
    {
      $conn->query("insert into criteria(criteria,subevent_id,percentage,criteria_ctr)values('$c2_name','$sub_event_id','$cp2','2')"); 
    }
    
    
       $c3_name=$_POST['crit3']; 
    $cp3=$_POST['cp3'];
    if($c3_name!="" or $cp3>0)
    {
      $conn->query("insert into criteria(criteria,subevent_id,percentage,criteria_ctr)values('$c3_name','$sub_event_id','$cp3','3')"); 
    }
    
    
       $c4_name=$_POST['crit4']; 
    $cp4=$_POST['cp4'];
   if($c4_name!="" or $cp4>0)
    {
      $conn->query("insert into criteria(criteria,subevent_id,percentage,criteria_ctr)values('$c4_name','$sub_event_id','$cp4','4')"); 
    }
    
    
       $c5_name=$_POST['crit5']; 
    $cp5=$_POST['cp5'];
    if($c5_name!="" or $cp5>0)
    {
      $conn->query("insert into criteria(criteria,subevent_id,percentage,criteria_ctr)values('$c5_name','$sub_event_id','$cp5','5')"); 
    }
    
    
       $c6_name=$_POST['crit6']; 
    $cp6=$_POST['cp6'];
    if($c6_name!="" or $cp6>0)
    {
      $conn->query("insert into criteria(criteria,subevent_id,percentage,criteria_ctr)values('$c6_name','$sub_event_id','$cp6','6')"); 
    }
    
    
       $c7_name=$_POST['crit7']; 
    $cp7=$_POST['cp7'];
   if($c7_name!="" or $cp7>0)
    {
      $conn->query("insert into criteria(criteria,subevent_id,percentage,criteria_ctr)values('$c7_name','$sub_event_id','$cp7','7')"); 
    }
    
    
       $c8_name=$_POST['crit8']; 
    $cp8=$_POST['cp8'];
    if($c8_name!="" or $cp8>0)
    {
      $conn->query("insert into criteria(criteria,subevent_id,percentage,criteria_ctr)values('$c8_name','$sub_event_id','$cp8','8')"); 
    }
    
    
       $c9_name=$_POST['crit9']; 
    $cp9=$_POST['cp9'];
   if($c9_name!="" or $cp9>0)
    {
      $conn->query("insert into criteria(criteria,subevent_id,percentage,criteria_ctr)values('$c9_name','$sub_event_id','$cp9','9')"); 
    }
    
    
       $c10_name=$_POST['crit10']; 
    $cp10=$_POST['cp10'];
    if($c10_name!="" or $cp10>0)
    {
      $conn->query("insert into criteria(criteria,subevent_id,percentage,criteria_ctr)values('$c10_name','$sub_event_id','$cp10','10')"); 
    }
    /* end criteria */
   

   
  
  
 ?>
  <script>

    window.location = 'home.php';
    alert('Organizer <?php echo $fname." ".$mname." ".$lname; ?> registered successfully!');						
  </script>
  <?php  
 
 
} ?>




  <?php
 if (isset($_POST['delete_cont']))
{

$org_pass = $_POST['org_pass'];

 $sub_event_id=$_POST['sub_event_id'];
    $se_name=$_POST['se_name'];
    
    
 if($check_pass==$org_pass){
    
 

    $id=$_POST['selector'];

    $N = count($id);
    for($i=0; $i < $N; $i++)
    {
 $conn->query("delete from contestants where contestant_id='$id[$i]'"); 
 
 $conn->query("delete from sub_results where contestant_id='$id[$i]'"); 
    }

  

  ?>
  <script>window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
    alert('Contestant(s) successfully deleted.');</script>
  <?php
}
else
{
      ?>
  <script>window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
    alert('Confirmation password is invalid!');</script>
  <?php
} }
?>




  <?php
 if (isset($_POST['delete_judge']))
{

$org_pass = $_POST['org_pass'];

 $sub_event_id=$_POST['sub_event_id'];
    $se_name=$_POST['se_name'];
    
    
 if($check_pass==$org_pass){
    
 

    $id=$_POST['selector'];

    $N = count($id);
    for($i=0; $i < $N; $i++)
    {
 $conn->query("delete from judges where judge_id='$id[$i]'"); 
 $conn->query("delete from sub_results where judge_id='$id[$i]'"); 
    }

 

  ?>
  <script>window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
    alert('Contestant(s) successfully deleted.');</script>
  <?php
}
else
{
      ?>
  <script>window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
    alert('Confirmation password is invalid!');</script>
  <?php
} }
?>



  <?php
 if (isset($_POST['delete_crit']))
{

$org_pass = $_POST['org_pass'];

 $sub_event_id=$_POST['sub_event_id'];
    $se_name=$_POST['se_name'];
    
    
 if($check_pass==$org_pass){
    
 

    $id=$_POST['selector'];

    $N = count($id);
    for($i=0; $i < $N; $i++)
    {
 $conn->query("delete from criteria where criteria_id='$id[$i]'"); 
 
    }

 

  ?>
  <script>window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
    alert('Criteria(s) successfully deleted.');</script>
  <?php
}
else
{
      ?>
  <script>window.location = 'sub_event_details_edit.php?sub_event_id=<?php echo $sub_event_id;?>&se_name=<?php echo $se_name;?>';
    alert('Confirmation password is invalid!');</script>
  <?php
} }
?>

  <?php include('footer.php'); ?>


  <!-- Le javascript
    ================================================== -->
  <!-- Placed at the end of the document so the pages load faster -->

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