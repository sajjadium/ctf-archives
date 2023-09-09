<?php

class Dbh {
   
    protected function connect() {
        try {
            if (!file_exists("/var/www/html/db.sqlite")) {
                $db = new PDO("sqlite:" . "/var/www/html/db.sqlite");
                $this->initDB();
            } else {
                $db = new PDO("sqlite:" . "/var/www/html/db.sqlite");
            }
            
            return $db;
        } catch (PDOException $e) {
            print "Error!: " . $e->getMessage() . "<br/>";
            die();
        }
    }

    private function initDB() {
        $hashedPwd = password_hash("FAKE_PASS_FOR_TESTING", PASSWORD_DEFAULT);

        $stmt = $this->connect()->prepare('CREATE TABLE IF NOT EXISTS users (
            user_id   INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            webhook TEXT NOT NULL,
            tmp_pass_time INTEGER DEFAULT NULL
            )');
        $stmt->execute();

        $stmt = $this->connect()->prepare('INSERT INTO users (username, password, webhook)
        VALUES ("admin", :password, :webhook)');
        $stmt->bindValue(':password', $hashedPwd);
        $stmt->bindValue(':webhook', "https://webhook.site/fake");
        $stmt->execute();
    }

}

?>
