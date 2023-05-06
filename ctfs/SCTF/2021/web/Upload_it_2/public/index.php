<?php
include_once "../vendor/autoload.php";

error_reporting(0);
session_start();

define("UPLOAD_PATH", "/tmp/sandbox");
if (!file_exists(UPLOAD_PATH)) {
    @mkdir(UPLOAD_PATH);
}

// emmm...easy backdoor
class sandbox {
	private $evil;
	public $upload_path;
	
	public function make_user_upload_dir() {
		$md5_dir = md5($_SERVER['REMOTE_ADDR'] . session_id());
		$this->upload_path = UPLOAD_PATH . "/" . $md5_dir;
		@mkdir($this->upload_path);
		$_SESSION["upload_path"] = $this->upload_path;
	}
	
	public function has_upload_dir() {
		return !empty($_SESSION["upload_path"]);
	}
	
	public function __wakeup() {
		/*
		I removed this code because it was too dangerous.
		*/
		throw new Error("NO NO NO");
	}
	
	public function __destruct() {
		/*
		I removed this code because it was too dangerous.
		*/
	}
	
	public function __call($func, $value) {
		if (method_exists($this, $func)) {
			call_user_func_array(
				[$this, $func],
				$value
			);
		}
	}
	
	private function backdoor() {
		// __destruct and __wakeup are deleted. It looks like backdoor should not be called.
		include_once $this->evil;
	}
}

$box = new sandbox();
if (!$box->has_upload_dir()) {
    $box->make_user_upload_dir();
}

if (!empty($_FILES['file'])) {
    $file = $_FILES['file'];
    if ($file['size'] < 1024 * 1024) {
        if (!empty($_POST['path'])) {
            $upload_file_path = $_SESSION["upload_path"]."/".$_POST['path'];
            $upload_file = $upload_file_path."/".$file['name'];
        } else {
            $upload_file_path = $_SESSION["upload_path"];
            $upload_file = $_SESSION["upload_path"]."/".$file['name'];
        }

        if (move_uploaded_file($file['tmp_name'], $upload_file)) {
            echo "OK! Your file saved in: " . $upload_file;
        } else {
            echo "emm...Upload failed:(";
        }
    } else {
        echo "too big!!!";
    }
} else if (!empty($_GET['phpinfo'])) {
    phpinfo();
    exit();
} else {
    echo <<<CODE
<html>
    <head>
        <title>Upload</title>
    </head>

    <body>
        <h1>Upload files casually XD</h1>
        <form action="index.php" method="post" enctype="multipart/form-data">
            FILE: <input type="file" name="file">
            PATH: <input type="text" name="path">
            <input type="submit">
        </form>

        <hr>

        <h3>or...Just look at the phpinfo?</h3>
        <a href="./index.php?phpinfo=1">go to phpinfo</a>
    </body>
</html>
CODE;
}