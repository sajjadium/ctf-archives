<?php

ini_set('display_errors', 0);
error_reporting(0);

class DB
{
    private static $instance = NULl;
    public static function getInstance() {
      if (!isset(self::$instance)) {
        try {
          $connectionString = "mysql:host=" . getenv('MYSQL_HOSTNAME') . ";dbname=" . getenv('MYSQL_DATABASE');
          self::$instance = new PDO($connectionString, getenv('MYSQL_USER'), getenv('MYSQL_PASSWORD'));
          self::$instance->exec("SET NAMES 'utf8'");
        } catch (PDOException $ex) {
          die($ex->getMessage());
        }
      }
      return self::$instance;
    }
}