  <!-- Footer
    ================================================== -->
    <footer class="footer">
      <div class="container">
      <center>
      
      <font size="4">Judging Management System &COPY; <?= date('Y') ?> </font>
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