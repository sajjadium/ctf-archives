<?php

session_start();

function get_pdo()
{
    $dsn="sqlite:/var/sqlite/sqlite.db";
    $pdo = new PDO($dsn, null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
    return $pdo;
}

function setup_db($pdo)
{   
    $already_setup = FALSE;
    try
    {
        $already_setup = $pdo->exec("select 1 from users inner join messages on users.id = messages.id");
    }
    catch(Exception $ex)
    {
        $already_setup = FALSE;
    }
    if($already_setup === FALSE)
    {
        $commands = [
        'CREATE TABLE IF NOT EXISTS `users` (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `username` varchar(255) NOT NULL UNIQUE, `password` varchar(255) NOT NULL, `role` varchar(255) NOT NULL default "user");',
        'CREATE TABLE IF NOT EXISTS `messages` (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, `title` varchar(255) NOT NULL, `content` varchar(512) NOT NULL, `file` varchar(512) NOT NULL default "", `created_at` timestamp default CURRENT_TIMESTAMP NOT NULL, `viewed` BOOLEAN DEFAULT 0, `user_id` INTEGER unsigned NOT NULL, FOREIGN KEY (`user_id`) REFERENCES users(`id`) ON DELETE CASCADE);',
        'INSERT INTO `users` (`username`, `password`, `role`) VALUES ("admin", "$2y$10$yerhXWb8EZR4MBHT0oOm2e1S2lTheH4zHOWqRIKTKEuVMyiL1Mtl6", "admin");'
        ];

        foreach($commands as $command)
        {
            $pdo->exec($command);
        }
    }
}

try
{
    $pdo = get_pdo();
    setup_db($pdo);
}
catch(Exception $e)
{
    die("Could not connect to the database! Please report to CTF admin!" . $e->getMessage());
}
?>
