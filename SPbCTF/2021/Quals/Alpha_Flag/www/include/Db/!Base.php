<?php
abstract class Db {
    private static $instance = NULL;

    static function Instance() {
        if (self::$instance === NULL) {
            $dbClass = "Db_" . Db_Config::$driver;
            self::$instance = new $dbClass(Db_Config::$hostname, Db_Config::$user, Db_Config::$password, Db_Config::$db);
        }

        return self::$instance;
    }

    abstract function __construct($hostname, $user, $password, $db);
    abstract protected function Prepare($query);
    abstract protected function Bind(&$statement, $parameter, $value);
    abstract protected function ExecuteAndFetch($statement);

    function Select($table, $columns = false, $filter = false) {
        if ($columns === false) {
            $columns = "*";
        }

        $whereClause = "";
        if ($filter !== false) {
            $whereClause = "WHERE " . implode(" AND ", array_map(function ($column) {
                return "`$column` = :$column";
            }, array_keys($filter)));
        }

        $query = new Misc_ProfanityFilter("SELECT $columns FROM `$table` $whereClause");
        $statement = $this->Prepare($query);

        if ($filter !== false) {
            foreach ($filter as $column => $value) {
                $this->Bind($statement, ":$column", new Misc_ProfanityFilter($value));
            }
        }

        return $this->ExecuteAndFetch($statement);
    }

    function Update($table, $columns, $filter = false) {
        $setClause = implode(", ", array_map(function ($column) {
            return "`$column` = :new_$column";
        }, array_keys($columns)));

        $whereClause = "";
        if ($filter !== false) {
            $whereClause = "WHERE " . implode(" AND ", array_map(function ($column) {
                return "`$column` = :old_$column";
            }, array_keys($filter)));
        }

        $query = new Misc_ProfanityFilter("UPDATE `$table` SET $setClause $whereClause");
        $statement = $this->Prepare($query);

        foreach ($columns as $column => $value) {
            $this->Bind($statement, ":new_$column", new Misc_ProfanityFilter($value));
        }
        if ($filter !== false) {
            foreach ($filter as $column => $value) {
                $this->Bind($statement, ":old_$column", new Misc_ProfanityFilter($value));
            }
        }

        return $this->ExecuteAndFetch($statement) !== false;
    }

    function Insert($table, $columns) {
        $columnsClause = implode(", ", array_map(function ($column) {
            return "`$column`";
        }, array_keys($columns)));

        $valuesClause = implode(", ", array_map(function ($column) {
            return ":$column";
        }, array_keys($columns)));

        $query = new Misc_ProfanityFilter("INSERT INTO `$table` ($columnsClause) VALUES ($valuesClause)");
        $statement = $this->Prepare($query);

        foreach ($columns as $column => $value) {
            $this->Bind($statement, ":$column", new Misc_ProfanityFilter($value));
        }

        return $this->ExecuteAndFetch($statement) !== false;
    }

    function __toString() {
        return "[" . __CLASS__ . "]";
    }
}
