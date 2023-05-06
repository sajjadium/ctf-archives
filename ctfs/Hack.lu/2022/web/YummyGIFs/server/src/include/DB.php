<?php

class DB
{
  private static mysqli $db;

  static public function buildMySQL()
  {
    $db_host = getenv('MYSQL_HOST');
    $db_user = getenv('MYSQL_USER');
    $db_pass = getenv('MYSQL_PASSWORD');
    $db_database = getenv('MYSQL_DATABASE');
    static::$db = new mysqli($db_host, $db_user, $db_pass, $db_database);
  }

  public static function getInstance()
  {
    return static::$db;
  }

  public static function connect_errno()
  {
    return static::$db->connect_errno;
  }

  public static function login($username, $password)
  {
    try {
      $stmt = static::$db->prepare('SELECT name, id, password FROM users WHERE name = BINARY ?');
      $stmt->bind_param('s', $username);
      $stmt->execute();
      $stmt->store_result();
      $stmt->bind_result($username, $user_id, $password_hash);
      if ($stmt->num_rows === 1) {
        $stmt->fetch();
        if (password_verify($password, $password_hash)) {
          return array('username' => $username, 'user_id' => $user_id);
        }
      }
    } catch (Exception $e) {
      // Don't leak DB errors.
    }
    throw new Exception('Invalid username or password');
  }

  public static function register($username, $password)
  {
    try {
      $stmt = static::$db->prepare('SELECT * FROM users WHERE name = BINARY ?');
      $stmt->bind_param('s', $username);
      $stmt->execute();
      $stmt->store_result();
    } catch (Exception $e) {
      throw new Exception('Database error');
    }
    if ($stmt->num_rows > 0) {
      throw new Exception('Username already taken');
    }
    try {
      $password = password_hash($password, PASSWORD_ARGON2ID);
      $stmt = static::$db->prepare('INSERT INTO users (name, password) VALUES (?, ?)');
      $stmt->bind_param('ss', $username, $password);
      $stmt->execute();
    } catch (Exception $e) {
      throw new Exception('Database error');
    }
    return true;
  }

  public static function saveGIF($random_id, $name, $title, $description, $user_id)
  {
    try {
      $stmt = static::$db->prepare('INSERT INTO gifs (random_id, name, title, description, user_id) VALUES (?, ?, ?, ?, ?)');
      $stmt->bind_param('ssssi', $random_id, $name, $title, $description, $user_id);
      $stmt->execute();
    } catch (Exception $e) {
      throw new Exception('Database error');
    }
  }

  public static function getGIFsByUser($user_id)
  {
    try {
      $stmt = static::$db->prepare('SELECT random_id, name, title, description FROM gifs WHERE user_id = ?');
      $stmt->bind_param('i', $user_id);
      $stmt->execute();
      $res = $stmt->get_result();
      return $res;
    } catch (Exception $e) {
      throw new Exception('Database error');
    }
  }

  public static function getGIFById($random_id) {
    try {
      $stmt = static::$db->prepare('SELECT name, title, description, random_id FROM gifs WHERE random_id = ?');
      $stmt->bind_param('s', $random_id);
      $stmt->execute();
      $stmt->store_result();
      $stmt->bind_result($name, $title, $description, $random_id);
      if ($stmt->num_rows === 1) {
        $stmt->fetch();
        return array('name' => $name, 'title' => $title, 'description' => $description, 'random_id' => $random_id);
      }
    } catch (Exception $e) {
      throw new Exception('Database error');
    }
    throw new Exception('GIF not found');
  }
}

DB::buildMySQL();
if (DB::connect_errno()) {
  echo ('Error while connecting to DB.');
  exit();
}
