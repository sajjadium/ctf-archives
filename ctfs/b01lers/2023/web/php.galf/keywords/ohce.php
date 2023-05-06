<?php

class ohce {
    public $args = array(NULL);
    public function __construct() {
        $this->args = NULL;
        $this->result = NULL;
    }

    public function __invoke($args, $arg_val) {
        $this->args = $args[$arg_val];
        $arg_val++;
        $parsable = array("orez_lum", "orez_dda");
        if (in_array($this->args, $parsable)) { // we can run operators in ohce!
            $class = new $this->args;
            $this->result = $class($args, $arg_val);
        } else {
            $this->result = $this->args;
        }
        $this->result = strrev($this->result) . "\n";
        echo $this->result;
    }
}
?>