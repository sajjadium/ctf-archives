<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<title>Insert and view using php, mysql and AJAX</title>
<script type="text/javascript" src="jquery.min.js"></script>
<script type="text/javascript">
$(function() {
$(".submit_button").click(function() {
var textcontent = $("#content").val();
var dataString = 'content='+ textcontent;
if(textcontent=='')
{
alert("Enter some text..");
$("#content").focus();
}
else
{
$("#flash").show();
$("#flash").fadeIn(400).html('<span class="load">Loading..</span>');
$.ajax({
type: "POST",
url: "action.php",
data: dataString,
cache: true,
success: function(html){
$("#show").after(html);
document.getElementById('content').value='';
$("#flash").hide();
$("#content").focus();
}  
});
}
return false;
});
});
</script>
<style type="text/css">
.container { 
width:500px; 
margin:0 auto; 
}
a{
text-decoration:none;
}
h2 {
font-size:20px; 
color:#03C;
}
.load {
color:#06C;
}
input { 
float:right;
}
.space { 
margin-bottom:25px; 
margin-top:10px;
}
.showbox { 
border-bottom:1px #09C solid; 
width:490px; 
color:#033;
font-weight:bold;
word-wrap:break-word;
padding:10px; 
font-size:14px; 
font-family:Tahoma, Geneva, sans-serif; 
margin-bottom:5px;
}
</style>
</head>

<body>
 
<div class="container">

<div class="main">
<form  method="post" name="form" action="">
<textarea style="width:500px; font-size:14px; height:60px; font-weight:bold; resize:none;" name="content" id="content" ></textarea><br />
<input type="submit" value="Post" name="submit" class="submit_button"/>
</form>
</div>
<div class="space"></div>
<div id="flash" align="left"  ></div>
<div id="show" align="left"></div>
</div>
</body>
</html>
