<?php
class Mail_Inbox {
    private $user, $storage;
    private $mails;

    function __construct($user) {
        $this->user = $user;
        list ($login) = explode("@", $user->GetLogin());
        $this->storage = Mail_Config::$mailDir . "/$login";
        $this->LoadData();
    }

    private function LoadData() {
        $this->mails = [];
        if (!is_file($this->storage)) {
            return;
        }
        $file = fopen($this->storage, "r");
        if ($file) {
            $mailData = "";
            do {
                $line = fgets($file);
                if ((substr($line, 0, 5) == "From " || feof($file)) && !empty($mailData)) {
                    $this->mails[] = new Mail(count($this->mails), $mailData);
                    $mailData = "";
                } else {
                    $mailData .= $line;
                }
            } while (!feof($file));
            fclose($file);
        }
    }

    function GetMail($id) {
        return isset($this->mails[$id]) ? $this->mails[$id] : false;
    }

    function __toString() {
        if (empty($this->mails)) {
            return "<tr><td colspan='3'><em>Your inbox is empty</em></td></tr>";
        }
        return implode("", array_reverse($this->mails));
    }
}
