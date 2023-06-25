<!DOCTYPE html>
<html lang="en">
   
   <?php
   
   include('header2.php');
   include('session.php');
  
  $txtsearch=$_POST['txtsearch'];
   
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
                        
                        <li><a href="rev_main_event.php">Data Reviews</a> / </li>
                        
                        <li>Data Reviews: Search</li>
                        
                    </ul>
                </div>
                
                
    <br />
    <div class="col-lg-1">
   </div>
    <div class="col-lg-10">
    
    <form method="POST" target="_self" action="review_search.php">
    
     <input style="font-size: large; height: 45px !important; text-indent: 7px !important;" class="form-control btn-block" name="txtsearch" placeholder="Enter a keyword and search..." value="<?php echo $txtsearch; ?>" />  
     <br />
      <button class="btn btn-info pull-right" style="width: 150px !important;"><i class="icon-search"></i> <strong>SEARCH</strong></button> 
     
      </form>
   </div>
   <div class="col-lg-1">
   </div>
 
  
  <div class="row">
      
      <div class="span12">

 <h3>Search Results for <i><ins><?php echo $txtsearch; ?></ins></i></h3>
        
        
  <hr />
  
  
       
    <!-- main event --> 
     
     
          
           
 <?php   
          $event_query = $conn->query("select * from main_event where event_name like '%$txtsearch%'") or die(mysql_error());
	 
            
     
     $menum_row = $event_query->rowcount();
        if( $menum_row > 0)
        { ?>
         <h3>Main Events</h3>
     	<?php while ($event_row = $event_query->fetch()) 
        {
            $search_mainevent_id=$event_row['mainevent_id'];
            ?>
          
           
         
          <table class="table table-bordered">
        <thead>
        
     <th><a title="click to view full details" target="_blank" href="print_all_results.php?main_event_id=<?php echo $search_mainevent_id; ?>"><?php echo $event_row['event_name']; ?> &raquo;</a></th>
       
       
         
        </thead>
     <tbody>
     
     
         
      
        
    
     </tbody>
     
          </table>
          
      <?php } } ?>
    
    
    <!-- sub event -->
    
    <?php   
          $event_query = $conn->query("select * from sub_event where event_name like '%$txtsearch%'") or die(mysql_error());
	 
           
     
     $menum_row = $event_query->rowcount();
        if( $menum_row > 0){ ?>
        <h3>Sub Events</h3>
        
        <?php 
        while ($event_row = $event_query->fetch()) 
        { 
             $search_mainevent_id=$event_row['mainevent_id'];
             $search_subevent_id=$event_row['subevent_id'];
            ?>
          
           
         
          <table class="table table-bordered">
        <thead>
        
     <th><a title="click to view full details" target="_blank" href="review_result.php?mainevent_id=<?php echo $search_mainevent_id; ?>&sub_event_id=<?php echo $search_subevent_id; ?>"><?php echo $event_row['event_name']; ?> &raquo;</a></th>
       
       
         
        </thead>
     <tbody>
     
     
         
      
        
    
     </tbody>
     
          </table>
          
      <?php } } ?>
      
      
        <!-- contestants -->  
      
      <?php   
          $event_query = $conn->query("select * from contestants where fullname like '%$txtsearch%'") or die(mysql_error());
	
     $menum_row = $event_query->rowcount();
        if( $menum_row > 0)
        { ?>
              <h3>Contestants</h3>
            <?php	while ($event_row = $event_query->fetch()) 
        { 
            $search_contestant_id=$event_row['contestant_id'];
     
     
            ?>
          
          
         
          <table class="table table-bordered">
        <thead>
        
     <th><a title="click to view full details" href="#"><?php echo $event_row['fullname']; ?> &raquo;</a></th>
       
       
         
        </thead>
     <tbody>
     
     
         
      
        
    
     </tbody>
     
          </table>
          
      <?php } } ?>
      
      
      <!-- judges -->  
      
      <?php   
          $event_query = $conn->query("select * from judges where fullname like '%$txtsearch%'") or die(mysql_error());
 
     $menum_row = $event_query->rowcount();
        if( $menum_row > 0)
        { ?>
        <h3>Judges</h3>
     	<?php while ($event_row = $event_query->fetch()) 
        { 
             $search_judge_id=$event_row['judge_id'];
             
            ?>
          
            
         
          <table class="table table-bordered">
        <thead>
        
     <th><a title="click to view full details" href="#"><?php echo $event_row['fullname']; ?> &raquo;</a></th>
       
       
         
        </thead>
     <tbody>
     
     
         
      
        
    
     </tbody>
     
          </table>
          
      <?php } } ?>
      
 
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
