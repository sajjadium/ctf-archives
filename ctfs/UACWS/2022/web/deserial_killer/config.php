<?php
    define('DEBUG', true);
    const PATH_TO_SQLITE_DB = 'app.db';
    $db_con = new PDO('sqlite:' . PATH_TO_SQLITE_DB);

    class User {
        public $username;
        public $picture_path;
        public $profile_pic;

        public function __construct($name, $path) {
            $this->username = $name;
            $this->picture_path = $path;
        }

        public function __wakeup() {
            $this->profile_pic = file_get_contents($this->picture_path);
        }
}

?>
