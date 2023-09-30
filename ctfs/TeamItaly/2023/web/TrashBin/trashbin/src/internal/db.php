<?php

function connectToDatabase()
{
    try {
        $dbh = new PDO('sqlite:/tmp/database.db', '', '', array(
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        ));
        $dbh->exec("
        CREATE TABLE IF NOT EXISTS `bin` (
            `id` VARCHAR(36) NOT NULL,
            `owner` VARCHAR(36) NOT NULL,
            `response_text` TEXT NOT NULL DEFAULT('Thank you for your trash!'),
            `response_headers` TEXT NOT NULL DEFAULT('{}'),
            `forward_request` BOOLEAN NOT NULL DEFAULT(FALSE),
            `forward_request_url` TEXT,
            `forward_request_headers` TEXT,
            `forward_request_body` TEXT
        );
        ");
        return $dbh;
    } catch (PDOException $e) {
        http_response_code(500);
        die;
    }
}
