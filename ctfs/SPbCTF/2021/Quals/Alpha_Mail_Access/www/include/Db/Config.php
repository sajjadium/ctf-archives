<?php
class Db_Config {
    static $driver = "Sqlite";
    static $hostname = "";
    static $user = "";
    static $password = "";
    static $db = "db/db.db";

    function __toString() {
        return "[" . __CLASS__ . ": " . self::$driver . "://" . self::$user . ":" . self::$password . "@" . self::$hostname . "/" . self::$db . "]";
    }
}
