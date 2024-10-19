 

<!DOCTYPE html>
<html lang="en">
  
  <?php 
    include('header2.php');
    include('session.php');
    
 $mainevent_id=$_POST['main_event_id'];

    
   	$mainevent_query = $conn->query("SELECT * FROM main_event where mainevent_id='$mainevent_id'") or die(mysql_error());
    while ($mainevent_row = $mainevent_query->fetch()) 
        {
            
            $m_event_name=$mainevent_row['event_name'];
        } 
  ?>
  
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
                <a href="selection.php">User Selection</a>
              </li>
 
                <li>
                <a href="home.php">List of Events</a>
              </li>
 
              <li>
                <a href="score_sheets.php">Score Sheets</a>
              </li>
              
            
               <li class="active">
                  <a href="rev_main_event.php"><strong>DATA REVIEWS</strong></a>
              </li>
 
              
              
              
                <li class="dropdown">
                  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">My Account <span class="caret"></span></a>
                  <ul class="dropdown-menu" role="menu">
 
              
              <li>
                  <a target="_blank" href="edit_organizer.php">Settings</a>
              </li>
 
              <li>
                <a href="logout.php">Logout <?php echo $name; ?></a>
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
    <h1>Data Reviews</h1>
    <p class="lead">Judging Management System</p>
  </div>
</header>

    <div class="container">
    
    <br />
                <div class="col-md-12">
                    <ul class="breadcrumb">
                    
                        <li><a href="selection.php">User Selection</a> / </li>
                    
                        <li><a href="home.php">List of Events</a> / </li>
                        
                        <li><a href="rev_main_event.php">DR: Main Event List</strong></i></a> / </li>
                        
                        <li>DR: Main Event <i><strong><?php echo $m_event_name; ?></strong></i> - Event List</li>
                        
                    </ul>
                </div>
                
                
    <br />
    <div class="col-lg-1">
   </div>
    <div class="col-lg-10">
    
    <form method="POST" target="_self" action="review_search.php">
    
     <input style="font-size: large; height: 45px !important; text-indent: 7px !important;" class="form-control btn-block" name="txtsearch" placeholder="Enter a keyword and search..." />  
     <br />
      <button class="btn btn-info pull-right" style="width: 150px !important;"><i class="icon-search"></i> <strong>SEARCH</strong></button> 
     
      </form>
   </div>
   <div class="col-lg-1">
   </div>

   
   <div class="col-lg-3">
   </div>
   <div class="col-lg-6">
 <div class="panel panel-primary">
            <div class="panel-heading">
              <h3 class="panel-title"><?php echo $m_event_name; ?> Event List</h3>
            </div>
  
     <div class="panel-body">
  
 <table class="table table-bordered">
  <thead>
  
   <th>Sub-Event</th>
  <th>Actions</th>
  </thead>
  
  
  <tbody>
   <?php    
   	$subevent_query = $conn->query("SELECT * FROM sub_event where mainevent_id='$mainevent_id'") or die(mysql_error());
    while ($subevent_row = $subevent_query->fetch()) 
        { ?>
  <tr>
  
  <td><?php echo $subevent_row['event_name']; ?></td>
  <td width="90">
  <a title="click to view event details" target="_blank"  href="review_result.php?mainevent_id=<?php echo $mainevent_id; ?>&sub_event_id=<?php echo $subevent_row['subevent_id']; ?>" class="btn btn-primary"><i class="icon-folder-open"></i></a>
  <a target="_blank" title="click to print event result" href="review_se_result.php?mainevent_id=<?php echo $mainevent_id; ?>&sub_event_id=<?php echo $subevent_row['subevent_id']; ?>" class="btn btn-info"><i class="icon-print"></i></a> 
  </td>
  
  </tr>
  <?php } ?>
 
  </tbody>
  </table>
 
</div>
 
          </div>
          
        
  </div>
  
 <div class="col-lg-3">
   </div>
 
 
          </div>
 

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
