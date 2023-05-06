<html>
	<head>
		<title>Secretsdump As Service</title>
		
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <style>
body { 
  width: 1000px; 
  margin: 100px auto; 
  background-color: #f5f5f5; 
}

.copyright {
  display:block;
  margin-top: 100px;
  text-align: center;
  font-family: Helvetica, Arial, sans-serif;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
}
.copyright a{
  text-decoration: none;
  color: #EE4E44;
}

.file-upload{display:block;text-align:center;font-family: Helvetica, Arial, sans-serif;font-size: 12px;}
.file-upload .file-select{display:block;border: 2px solid #dce4ec;color: #34495e;cursor:pointer;height:40px;line-height:40px;text-align:left;background:#FFFFFF;overflow:hidden;position:relative;}
.file-upload .file-select .file-select-button{background:#dce4ec;padding:0 10px;display:inline-block;height:40px;line-height:40px;}
.file-upload .file-select .file-select-name{line-height:40px;display:inline-block;padding:0 10px;}
.file-upload .file-select:hover{border-color:#34495e;transition:all .2s ease-in-out;-moz-transition:all .2s ease-in-out;-webkit-transition:all .2s ease-in-out;-o-transition:all .2s ease-in-out;}
.file-upload .file-select:hover .file-select-button{background:#34495e;color:#FFFFFF;transition:all .2s ease-in-out;-moz-transition:all .2s ease-in-out;-webkit-transition:all .2s ease-in-out;-o-transition:all .2s ease-in-out;}
.file-upload.active .file-select{border-color:#3fa46a;transition:all .2s ease-in-out;-moz-transition:all .2s ease-in-out;-webkit-transition:all .2s ease-in-out;-o-transition:all .2s ease-in-out;}
.file-upload.active .file-select .file-select-button{background:#3fa46a;color:#FFFFFF;transition:all .2s ease-in-out;-moz-transition:all .2s ease-in-out;-webkit-transition:all .2s ease-in-out;-o-transition:all .2s ease-in-out;}
.file-upload .file-select input[type=file]{z-index:100;cursor:pointer;position:absolute;height:100%;width:100%;top:0;left:0;opacity:0;filter:alpha(opacity=0);}
.file-upload .file-select.file-select-disabled{opacity:0.65;}
.file-upload .file-select.file-select-disabled:hover{cursor:default;display:block;border: 2px solid #dce4ec;color: #34495e;cursor:pointer;height:40px;line-height:40px;margin-top:5px;text-align:left;background:#FFFFFF;overflow:hidden;position:relative;}
.file-upload .file-select.file-select-disabled:hover .file-select-button{background:#dce4ec;color:#666666;padding:0 10px;display:inline-block;height:40px;line-height:40px;}
.file-upload .file-select.file-select-disabled:hover .file-select-name{line-height:40px;display:inline-block;padding:0 10px;}
			</style>
</head>
<body>
<?php
//error_reporting(-1);
//ini_set('display_errors', 'On');

require_once("utils.php");

if (isset($_POST["bootkey"]) && $_POST["bootkey"]!= "" ){
  if (!ctype_alnum($_POST["bootkey"])){
    echo "Invalid character in boot key";
    exit;
  }
  $bootkey = $_POST["bootkey"];
}else{
  $bootkey ="";
}

if(isset($_POST['submit'])){
	$uploadOk=true;
	$target_dir = "uploads/";
	$randomStringFilename = generateRandomString();
	foreach (array("system", "security") as $file){
	$target_file = $target_dir . $file."-". $randomStringFilename;
	if ($file == "system" && isset($_POST["bootkey"]) && $_POST["bootkey"]!= ""){
    $bootkey = $_POST["bootkey"];
    continue;
  }
	if ($_FILES[$file]["size"] > 20000000) {
		echo "Sorry, your file $file is too large.<br />";
		$uploadOk = false;
	  }
  	if ($_FILES[$file]["size"] == 0) {
		echo "Sorry, your file $file is empty.<br />";
		$uploadOk = false;
	  }
	  if ($uploadOk && move_uploaded_file($_FILES[$file]["tmp_name"], $target_file)) {
		//echo "The file ". htmlspecialchars( basename( $_FILES[$file]["name"])). " has been uploaded.<br />";
	  } else {
		echo "Sorry, there was an error uploading your file.<br />";
	  }
	}
	
  if ($uploadOk){

  
  if ($bootkey != ""){
	  $svcPassword = shell_exec("secretsdump.py  -security ".$target_dir."/security-".$randomStringFilename." -bootkey ".$bootkey." LOCAL | grep ' _SC_' -A 1 -a | grep -v '[*]' -a| cut -d':' -f 2");
  }else{
	  $svcPassword = shell_exec("secretsdump.py  -security ".$target_dir."/security-".$randomStringFilename." -system ".$target_dir."/system-".$randomStringFilename." LOCAL | grep ' _SC_' -A 1 -a | grep -v '[*]' -a| cut -d':' -f 2");
    $bootkey = shell_exec("secretsdump.py  -security ".$target_dir."/security-".$randomStringFilename." -system ".$target_dir."/system-".$randomStringFilename." LOCAL | grep bootKey | cut -d'x' -f 2  ");

	  unlink($target_dir."/system-".$randomStringFilename);
  }
	unlink($target_dir."/security-".$randomStringFilename);

	if ($svcPassword != "") {
		$link = mysqlConnect();
	foreach ( preg_split("/((\r?\n)|(\r\n?))/", $svcPassword) as $password){
    $match = false;
		if ($password == "") {
			continue;
		}
		
		$result = checkPassword($link,$password);
		while ($obj = $result->fetch_object()) {
      $match = true;
			printf("<div class=\"alert alert-danger\" role=\"alert\">There is a match for <b>%s</b></div><br />\n", $password);
		}
    if (!$match) {
      printf("<div class=\"alert alert-success\" role=\"alert\">No match for <b>%s</b></div><br />\n", $password);
    }
	}
	mysqlDisconnect($link);
}

  echo "
  <br />
  <hr>";
}
}

?>
<br />
<div class="alert alert-primary" role="alert">
Below, secretsdump as a service, you don't want to install secretsdump we have your back.<br />
Upload your SECURITY and SYSTEM dump, secretsdump will retrieve all the passwords in LSA secrets and tell you if it's in popular wordlists and in my custom wordlists ;-).<br /><br />
You can find two example file: <a href="/system">system</a> and <a href="security">security</a>, the corresponding boot key is <b>3fe6404afd01286425e617225e6976e1</b>
</div>
<br />
<br />

<form method="POST" enctype="multipart/form-data">
<div class="form-group file-upload file-upload-security">
  <div class="file-select">
    <div class="file-select-button" id="fileName">Security File</div>
    <div class="file-select-name" id="noFileSecurity">No file chosen...</div> 
    <input type="file" name="security" id="chooseFileSecurity" required>
  </div>
</div>

<div class="form-row form-group ">


<div class="file-upload file-upload-system col-md-6">
  <div class="file-select">
    <div class="file-select-button" id="fileName">System File  </div>
    <div class="file-select-name" id="noFileSystem">No file chosen...</div> 
    <input type="file" name="system" id="chooseFileSystem">
  </div>
</div>
<div class="col-md-6">
<label class="sr-only" for="formBootkey">Boot key</label>
  <div class="input-group mb-2 mr-sm-2">
    <div class="input-group-prepend">
      <div class="input-group-text">Boot key</div>
    </div>
    <input type="text" class="form-control" id="formBootkey" name="bootkey" value="<?php echo $bootkey; ?>" placeholder="Boot key">
  </div>
    </div>
    <small> The system file is only used to get the boot key. To optimize the bandwith usage please prefer to enter the bootkey instead uploading the file</small>
</div>

<div>
  <button type="submit" name="submit" class="btn btn-primary" ng-click="vm.upload()" ng-disabled="!vm.file">Upload</button>
</div>
</form>

<script type="text/javascript" src="//code.jquery.com/jquery-1.10.2.min.js"></script>
<script>
$('#chooseFileSecurity').bind('change', function () {
  var filename = $("#chooseFileSecurity").val();
  if (/^\s*$/.test(filename)) {
    $(".file-upload-security").removeClass('active');
    $("#noFileSecurity").text("No file chosen..."); 
  }
  else {
    $(".file-upload-security").addClass('active');
    $("#noFileSecurity").text(filename.replace("C:\\fakepath\\", "")); 
  }
});

	$('#chooseFileSystem').bind('change', function () {
  var filename = $("#chooseFileSystem").val();
  if (/^\s*$/.test(filename)) {
    $(".file-upload-system").removeClass('active');
    $("#noFileSystem").text("No file chosen..."); 
  }
  else {
    $(".file-upload-system").addClass('active');
    $("#noFileSystem").text(filename.replace("C:\\fakepath\\", "")); 
  }
});
</script>
</body>
</html>
