<?php
class Mail_Config {
    static $mailDir = "/var/spool/mail";

    function __toString() {
        return "[" . __CLASS__ . ": " . self::$mailDir . "]";
    }
}
