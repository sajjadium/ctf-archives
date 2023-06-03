<?php
require_once('visualizer.php');

class MD5DBEngine {
    private $HashString = "";
    private $objArray = array();

    public function __construct($HashString) {
        $this->HashString = $HashString;
        $this->objArray['obj'] = $this;
    }

    public function perform() {
        include('db_connector.php');

        $query = "SELECT 'FOUND IN DB, UPDATE YOUR PASSWORDS!!' FROM UnsecurePasswordsHash WHERE value = '" . $this->HashString . "'";

        $db->exec($query);
        $res = $db->query($query)->fetchArray();
        return ($res[0]);
    }

    public function __toString() {
        return strval($this->objArray['obj']->perform());
    }
}
?>