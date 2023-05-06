<?php
class Db_Sqlite extends Db {
    private $pdo;

    function __construct($hostname, $user, $password, $db) {
        $this->pdo = new PDO("sqlite:$db");
    }

    function Prepare($query) {
        return $this->pdo->prepare($query);
    }

    function Bind(&$statement, $parameter, $value) {
        $valueType = PDO::PARAM_STR;
        if (is_numeric($value)) {
            $valueType = PDO::PARAM_INT;
        } elseif (is_bool($value)) {
            $valueType = PDO::PARAM_BOOL;
        }
        return $statement->bindValue($parameter, $value);
    }

    function ExecuteAndFetch($statement) {
        $result = $statement->execute();
        if (! $result) {
            return false;
        }
        return $statement->fetchAll();
    }
}
