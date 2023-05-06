<?php
class Smtp_Config {
    static $host = "127.0.0.1";
    static $port = 25;

    function __toString() {
        return "[" . __CLASS__ . ": " . self::$host . ":" . self::$port . "]";
    }
}
