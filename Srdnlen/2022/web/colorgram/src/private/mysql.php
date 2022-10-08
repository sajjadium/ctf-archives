<?php
class MySQLobject{
    private $connection;
    private $connected;

    function __construct(){
        $servername = "db";
        $database = getenv("MYSQL_DATABASE");
        $username = "root";
        $password = getenv("MYSQL_ROOT_PASSWORD");

        $this->connection = new mysqli($servername, $username, $password, $database);
        if($this->connection->connect_error){
            $this->connected = false;
            die('{"error":"cant connect to database"}');
        }else{
            $this->connected = true;
        }
    }

    function check_username($username){
        $query = $this->connection->prepare("select * from users where name=?");
        $query->bind_param("s", $username);
        $query->execute();
        if($query->get_result()->num_rows > 0){
            return true; // username already taken
        }
        return false; // username not taken
    }

    function register($username, $email, $password, $description){
        if(!$this->connected){
            die('{"error":"database not connected!"}');
        }

        if($this->check_username($username)){
            die('{"error":"username already taken!"}');
        }
        try{
            $query = $this->connection->prepare("INSERT INTO users(name, email, password, description) VALUES (?, ?, ?, ?)");
            $query->bind_param("ssss", $username, $email, $password, $description);
            $query->execute();
        }catch(Exception $e){
            die('{"error":"Something went wrong in the database!"}');
            return;
        }
        return;
    }   

    function verify_login($username, $password){
        try{
            $query = $this->connection->prepare("select * from users where name = ? and password = ?");
            $query->bind_param("ss", $username, $password);
            $query->execute();
            $res = $query->get_result();
            if($res->num_rows > 0){
                return true;
            }
            return false;
        }catch(Exception $e){
            die('{"error":"invalid sql query"}');
        }
    }


    function get_data($username){
        $query = $this->connection->prepare("select * from users where name = ?");
        $query->bind_param('s',$username);
        $query->execute();
        $res = $query->get_result()->fetch_assoc();
        return array(
            'username' => $res['name'],
            'email' => $res['email'],
            'description' => $res['description']

        );
    }

    function change_description($name, $newdesc){
        $query = $this->connection->prepare("update users set description = ? where name = ?");
        $query-> bind_param('ss', $newdesc, $name);
        $query->execute();
    }
}
?>