<?php
ob_start();
include("config.php");
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>EzCMS</title>
</head>

<body>
<h2>Upload platform</h2>
<div>
    <p>Upload it?</p>
</div>

<form action="upload.php" method="post" enctype="multipart/form-data">
    <label for="file">filename：</label>
    <input type="file" name="file" id="file"><br>
    <input type="submit" name="upload" value="提交">
</form>
</body>

</html>


<?php
if (isset($_FILES['file'])){
    $file_tmp = $_FILES['file']['tmp_name'];
    $file_name = $_FILES['file']['name'];
    $file_size = $_FILES['file']['size'];
    $file_error = $_FILES['file']['error'];
    if ($file_error > 0){
        die("something error");
    }
    $admin = new Admin($file_name, $file_tmp, $file_size);
    $admin->upload_file();
}else{
    $sandbox = 'sandbox/'.md5($_SERVER['REMOTE_ADDR']);
    if (!file_exists($sandbox)){
        mkdir($sandbox, 0777, true);
    }
    if (!is_file($sandbox.'/.htaccess')){
        file_put_contents($sandbox.'/.htaccess', 'lolololol, i control all');
    }
    echo "view my file : "."<br>";
    $path = "./".$sandbox;
    $dir = opendir($path);
    while (($filename = readdir($dir)) !== false){
        if ($filename != '.' && $filename != '..'){
            $files[] = $filename;
        }
    }
    foreach ($files as $k=>$v){
        $filepath = $path.'/'.$v;
        echo <<<EOF
        <div style="width: 1000px; height: 30px;">
        <Ariel>filename: {$v}</Ariel>
        <a href="view.php?filename={$v}&filepath={$filepath}">view detail</a>
</div>
EOF;
    }
    closedir($dir);

}
ob_end_flush();
