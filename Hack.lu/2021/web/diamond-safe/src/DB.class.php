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

    public static function prepare($query, $args){
        if (is_null($query)){
            return;
        }
        if (strpos($query, '%') === false){
            error('%s not included in query!');
            return;
        }

        // get args
        $args = func_get_args();
        array_shift( $args );

        $args_is_array = false;
        if (is_array($args[0]) && count($args) == 1 ) {
            $args = $args[0];
            $args_is_array = true;
        }

        $count_format = substr_count($query, '%s');

        if($count_format !== count($args)){
            error('Wrong number of arguments!');
            return;
        }
        // escape
        foreach ($args as &$value){
            $value = static::$db->real_escape_string($value);
        }

        // prepare
        $query = str_replace("%s", "'%s'", $query);
        $query = vsprintf($query, $args);
        return $query;

    }
    public static function commit($query){
        $res = static::$db->query($query);
        if($res !== false){ 
                return $res;
            }
            else{
                error('Error in query.');
        }
    }

    public static function create_db(){
        self::commit('CREATE TABLE IF NOT EXISTS users (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            name TEXT, 
            password TEXT
        ) 
        DEFAULT CHARSET=utf8;');

        self::commit('CREATE TABLE IF NOT EXISTS vault (
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            name TEXT,
            email TEXT,
            password TEXT
        ) 
        DEFAULT CHARSET=utf8;');
    }
}
?>