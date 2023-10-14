<?php

error_reporting(0);
highlight_file(__FILE__);

class memberISITDTU
{
    private $username = "onsra";
    private $password = "onsra";
    private $isAdmin = false;
    private $class = "info";

    function __construct()
    {
        $this->class = new info();
    }
    public function login($u, $p)
    {
        return $this->username === $u && $this->password === $p;
    }
    function __destruct()
    {
        if ($this->isAdmin && $this->username === "admin") {
            return $this->class->getInfo();
        }
    }
}

class info
{
    public $user = "onsra";
    public function getInfo()
    {
        return $this->user;
    }
}

class isitDtu
{
    function encodeData()
    {
        foreach ($_POST as $key => $value) {
            $_POST[$key] = pack("H*", substr($value, 13, -1));
        }
        @$encodedPost = base64_encode($_POST["onsra"]);
        @$decodedPost = base64_decode(@$encodedPost);
        if(!preg_match("/^[(0-9).^;]+$/",$decodedPost)){
            die("Baka baka");
        }
        return $decodedPost;
    }

    function getInfo()
    {
        return eval($this->encodeData());
    }
}


if (strpos($_SERVER['REQUEST_URI'], '_')){
    die("Baka baka");
}
if (isset($_GET["user_name"]) && isset($_GET["user_pass"])) {
    if ($_COOKIE["user"]) {
        $user = unserialize($_COOKIE["user"]);
    }
    $user->login("xxxx", "xxxx");
}
?>
