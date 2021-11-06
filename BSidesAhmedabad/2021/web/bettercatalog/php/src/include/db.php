<?php

$pdo = new PDO("mysql:host=" . $_ENV["MYSQL_HOST"] . ";dbname=" . $_ENV["MYSQL_DATABASE"], $_ENV["MYSQL_USER"], $_ENV["MYSQL_PASSWORD"]);
