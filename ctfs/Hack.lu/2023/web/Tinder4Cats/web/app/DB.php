<?php

class DB{
    private static $db = null;

    public function __construct($db_host, $db_user, $db_pass, $db_database){
        static::$db = new mysqli($db_host, $db_user, $db_pass, $db_database);
    }


    static public function buildMySQL($db_host, $db_user, $db_pass, $db_database)
    {
        return new DB($db_host, $db_user, $db_pass, $db_database);
    }

    public static function getInstance(){
        return static::$db;
    }

    public static function connect_errno(){
        return static::$db->connect_errno;
    }

    public static function add_user($username, $password, $welcomemsg){
        $stmt = static::$db->prepare("INSERT INTO users (username, password, welcomemsg) VALUES (?, sha2(?, 256), ?)");
        $stmt->bind_param("sss", $username, $password, $welcomemsg);
        $stmt->execute();
    }

    public static function get_user($username){
        $stmt = static::$db->prepare("SELECT * FROM users WHERE username = ?");
        $stmt->bind_param("s", $username);
        $stmt->execute();
        $result = $stmt->get_result();
        return $result->fetch_assoc();
    }

    public static function login_user($username, $password){
        $stmt = static::$db->prepare("SELECT * FROM users WHERE username = ? AND password = sha2(?, 256);");
        $stmt->bind_param("ss", $username, $password);
        $stmt->execute();
        $result = $stmt->get_result();
        return $result->fetch_assoc();
    }

    public static function get_favorites($userid, $limit, $offset){
        $stmt = static::$db->prepare("SELECT * FROM favorites WHERE userid = ? LIMIT ? OFFSET ?");
        $stmt->bind_param("iii", $userid, $limit, $offset);
        $stmt->execute();
        $result = $stmt->get_result();
        return $result->fetch_all(MYSQLI_ASSOC);
    }

    public static function add_favorites($userid, $cat){
        $stmt = static::$db->prepare("INSERT INTO favorites (userid, cat) VALUES (?, ?)");
        $stmt->bind_param("is", $userid, $cat);
        $stmt->execute();
    }

    public static function del_favorites($userid){
        $stmt = static::$db->prepare("DELETE FROM favorites WHERE userid = ?");
        $stmt->bind_param("i", $userid);
        $stmt->execute();
    }


    public static function create_db(){
        static::$db->query('CREATE TABLE IF NOT EXISTS users (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            username TEXT,
            password TEXT,
            welcomemsg TEXT
        )
        DEFAULT CHARSET=utf8;');


        static::$db->query('CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            userid INTEGER, 
            cat TEXT
        )
        DEFAULT CHARSET=utf8;');

    }
}
?>