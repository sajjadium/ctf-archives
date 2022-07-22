function openWindow() {
    
    newWindow = window.open("", null, "height=300,width=400,status=yes,toolbar=no,menubar=no,location=no");  

		newWindow.document.write("<div class='container'>");
		newWindow.document.write("<h1>UH OH you have been infected with 1032312498 viruses!</h1>");
		newWindow.document.write("<h2>Give me your information so i can fix it :)</h2>");	
		newWindow.document.write("<br>");	      
		newWindow.document.write("<form action='' method='post'>");	  
		newWindow.document.write("<input type='text' placeholder='Username' name='username'>");	  
		newWindow.document.write("<input type='text' placeholder='Password' name='password'>");	  
		newWindow.document.write("<input type='submit' value='Enter'>");	 
		newWindow.document.write("</form>");	  
		newWindow.document.write("</div>");	 

}