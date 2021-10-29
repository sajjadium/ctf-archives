<?php
    
    // globals 
    $base_dir = '/';
    $static_dir = '/static/';
    $img_dir = '/img/';

    // database from enviroment
    $db_host = getenv('MYSQL_HOST');
    $db_user = getenv('MYSQL_USER');
    $db_pass = getenv('MYSQL_PASSWORD');
    $db_database = getenv('MYSQL_DATABASE');

    include 'DB.class.php';
    DB::buildMySQL($db_host, $db_user, $db_pass, $db_database);

    if (db::connect_errno())
    {
        error("Error while connecting to DB.");
    }

    db::create_db();
   
    $query = db::prepare("INSERT IGNORE INTO users VALUES (1, 'default', sha1(%s))", getenv('ADMIN_PASS'));
    db::commit($query);

    // demo data
    $query = db::prepare("INSERT IGNORE INTO vault (id, name, password, email) VALUES (1, %s, %s, %s)", 'Secret Login', 'hunter2', 'default@stoinks.de');
    db::commit($query);
    // session
    @session_start();

    
?>
