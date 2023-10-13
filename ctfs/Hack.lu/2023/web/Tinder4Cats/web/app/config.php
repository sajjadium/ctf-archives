<?php

    header("Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-eval'; img-src * data:; connect-src *; frame-ancestors 'none';");
    header('Cross-Origin-Opener-Policy: same-origin');
    
    include 'DB.php';
    DB::buildMySQL(getenv('MYSQL_HOST'), getenv('MYSQL_USER'), getenv('MYSQL_PASSWORD'), getenv('MYSQL_DATABASE'));

    if (db::connect_errno())
    {
        die("Error while connecting to DB.");
    }

    db::create_db();
    // create accounts for ferderated login, passwords are not used
    db::add_user('admin', random_bytes(20), 'The flag is ' . getenv('FLAG') . '.');
    db::add_user('guest', random_bytes(20), 'Not allowed to see the flag.');

    // session
    ini_set('session.cookie_httponly', 1);
    @session_start();

    
?>
