<?php
error_reporting(0);
@session_start();
$sandbox_dir = 'sandbox/'. md5($_SERVER['REMOTE_ADDR']);
global $sandbox_dir;

function login(){

    $secret = "E3ry7Hjq";
    setcookie("hash", md5($secret."adminadmin"));
    return 1;

}

function is_admin(){
    $secret = "E3ry7Hjq";
    $username = $_SESSION['username'];
    $password = $_SESSION['password'];
    if ($username == "admin" && $password != "admin"){
        if ($_COOKIE['user'] === md5($secret.$username.$password)){
            return 1;
        }
    }
    return 0;
}

class Check{
    public $filename;

    function __construct($filename)
    {
        $this->filename = $filename;
    }

    function check(){
        $content = file_get_contents($this->filename);
        $black_list = ['system','eval','exec','+','passthru','`','assert'];
        foreach ($black_list as $k=>$v){
            if (stripos($content, $v) !== false){
                die("your file make me scare");
            }
        }
        return 1;
    }
}

class File{

    public $filename;
    public $filepath;
    public $checker;

    function __construct($filename, $filepath)
    {
        $this->filepath = $filepath;
        $this->filename = $filename;
    }

    public function view_detail(){

        if (preg_match('/^(phar|compress|compose.zlib|zip|rar|file|ftp|zlib|data|glob|ssh|expect)/i', $this->filepath)){
            die("nonono~");
        }
        $mine = mime_content_type($this->filepath);
        $store_path = $this->open($this->filename, $this->filepath);
        $res['mine'] = $mine;
        $res['store_path'] = $store_path;
        return $res;

    }

    public function open($filename, $filepath){
        $res = "$filename is in $filepath";
        return $res;
    }

    function __destruct()
    {
        if (isset($this->checker)){
            $this->checker->upload_file();
        }
    }

}

class Admin{
    public $size;
    public $checker;
    public $file_tmp;
    public $filename;
    public $upload_dir;
    public $content_check;

    function __construct($filename, $file_tmp, $size)
    {
        $this->upload_dir = 'sandbox/'.md5($_SERVER['REMOTE_ADDR']);
        if (!file_exists($this->upload_dir)){
            mkdir($this->upload_dir, 0777, true);
        }
        if (!is_file($this->upload_dir.'/.htaccess')){
            file_put_contents($this->upload_dir.'/.htaccess', 'lolololol, i control all');
        }
        $this->size = $size;
        $this->filename = $filename;
        $this->file_tmp = $file_tmp;
        $this->content_check = new Check($this->file_tmp);
        $profile = new Profile();
        $this->checker = $profile->is_admin();
    }

    public function upload_file(){

        if (!$this->checker){
            die('u r not admin');
        }
        $this->content_check -> check();
        $tmp = explode(".", $this->filename);
        $ext = end($tmp);
        if ($this->size > 204800){
            die("your file is too big");
        }
        move_uploaded_file($this->file_tmp, $this->upload_dir.'/'.md5($this->filename).'.'.$ext);
    }

    public function __call($name, $arguments)
    {

    }
}

class Profile{

    public $username;
    public $password;
    public $admin;

    public function is_admin(){
        $this->username = $_SESSION['username'];
        $this->password = $_SESSION['password'];
        $secret = "E3ry7Hjq";
        if ($this->username === "admin" && $this->password != "admin"){
            if ($_COOKIE['user'] === md5($secret.$this->username.$this->password)){
                return 1;
            }
        }
        return 0;

    }
    function __call($name, $arguments)
    {
        $this->admin->open($this->username, $this->password);
    }
}
