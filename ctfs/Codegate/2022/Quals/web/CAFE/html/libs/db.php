<?php
  function query($query, $param=[]){
    $dsn = 'mysql:host=mysql;port=3306;dbname=app;charset=utf8';
    try{
      $db = new PDO($dsn, 'app', 'c546cfcba41c26715fc8c3caa7527832');
      $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

      $db->exec('set sql_mode="STRICT_TRANS_TABLES"');

      $state = $db->prepare($query);
      $state->setFetchMode(PDO::FETCH_ASSOC);

      $result = array();
      $result['ret'] = $state->execute($param);
      $result['val'] = $state->fetch();
      $db = null;

      return $result;
    }catch(Exception $e){
      echo $e->getMessage();
    }
  }

  function query_all($query, $param=[]){
    $dsn = 'mysql:host=mysql;port=3306;dbname=app;charset=utf8';
    try{
      $db = new PDO($dsn, 'app', 'c546cfcba41c26715fc8c3caa7527832');
      $db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

      $db->exec('set sql_mode="STRICT_TRANS_TABLES"');

      $state = $db->prepare($query);
      $state->setFetchMode(PDO::FETCH_ASSOC);

      $result = array();
      $result['ret'] = $state->execute($param);
      $result['all'] = $state->fetchAll();
      $db = null;

      return $result;
    }catch(Exception $e){
      echo $e->getMessage();
    }
  }
?>