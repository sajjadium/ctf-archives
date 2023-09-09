<?php

class Signup extends Dbh {

    protected function checkUser($uid) {
        $stmt = $this->connect()->prepare('SELECT COUNT(*) FROM users where username = :username');
        $stmt->bindValue(':username', $uid);
        if (!$stmt->execute()) {
            $stmt = null;
            header("location: ../login.php?error=stmtfaild");
            exit();
        }
        
        if ($stmt->fetchColumn() > 0) {
            return false;
        } else {
            return true;
        }
    }

    protected function setUser($uid, $pwd, $wh) {
        $stmt = $this->connect()->prepare('INSERT INTO users (username, password, webhook) VALUES (:username, :password, :webhook)');

        $hashedPwd = password_hash($pwd, PASSWORD_DEFAULT);
        $stmt->bindValue(':username', $uid);
        $stmt->bindValue(':password', $hashedPwd);
        $stmt->bindValue(':webhook', $wh);
        
        if (!$stmt->execute()) {
            $errorInfo = $stmt->errorInfo();
            $stmt = null;
            header("location: ../login.php?error=" . $errorInfo[2]);
            exit();
        }

        $stmt = null;
    }

}

class SignupController extends Signup {

    private $uid;
    private $pwd;
    private $wh;

    public function __construct($uid, $pwd, $wh) {
        $this->uid = htmlspecialchars($uid);
        $this->pwd = $pwd;
        $this->wh = filter_var($wh, FILTER_SANITIZE_URL);
    }

    public function signupUser() {
        if (empty($this->uid) || empty($this->pwd) || empty($this->wh)) {
            header("location: ../login.php?error=EmptyInput");
            exit();
        }

        if (preg_match("/^[a-zA-Z0-9]*%/", $this->uid)) {
            header("location: ../login.php?error=InvalidUid");
            exit();
        }

        if (!filter_var($this->wh, FILTER_VALIDATE_URL)) {
            header("location: ../login.php?error=NotValidWebhook");
            exit();
        }

        if (!$this->checkUser($this->uid)) {
            header("location: ../login.php?error=UserTaken");
            exit();
        }

        $this->setUser($this->uid, $this->pwd, $this->wh);

    }

}


?>