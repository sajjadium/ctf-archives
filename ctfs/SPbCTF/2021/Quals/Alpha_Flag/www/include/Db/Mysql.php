<?php
class Db_Mysql extends Db {
    private $link;

    function __construct($hostname, $user, $password, $db) {
        $this->link = mysql_connect($hostname, $user, $password);
        mysql_select_db($db, $this->link);
    }

    function Prepare($query) {
        return $query;
    }

    function Bind(&$statement, $parameter, $value) {
        $statement = str_replace($parameter, "'" . mysql_real_escape_string($value, $this->link) . "'");
        return $statement;
    }

    function ExecuteAndFetch($statement) {
        $result = mysql_query($statement, $this->link);
        if (! $result) {
            return false;
        }

        $rows = [];
        while ($row = mysql_fetch_assoc($result)) {
            $rows[] = $row;
        }
        return $rows;
    }
}
