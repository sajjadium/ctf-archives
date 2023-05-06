<?php
    require "exceptions/throwable.php";
    require "parser/parsable.php";
    error_reporting(1); //only my custom errors >:)
    class syntaxreader {
        public $code = array(NULL);
        public $args = NULL;
        public $result = NULL;
        public function __construct($lines, $args, $debug = NULL) {
            $this->code = explode("\n", $lines);
            $this->args = $args;
            $this->result = $result;
            if (isset($debug)) {
                // disable debugging mode
                throw new noitpecxe(...$debug);
            }
        }
        public function run() {
            $this->parse();
        }
        public function parse() {
            $parsable = array("ohce");
            $arg_val = 0;
            $code = $this->code;
            $args = $this->args;
            $result = $this->result;
            for ($i = 0; $i < count($code); $i++) {
                $code[$i] = trim($code[$i]);
            }
            $args = explode(",", $args);
            for ($i = 0; $i < count($args); $i++) {
                $args[$i] = trim($args[$i]);
            }
            for ($i = 0; $i < count($code); $i++) {
                $token = explode(" ", $code[$i]);
                for ($j = 0; $j < count($token); $j++) {
                    try {
                        if (!in_array($token[$j], $parsable)) {
                            throw new noitpecxe("Non-Parsable Keyword!\n", 101);
                        }
                        if ($args[$arg_val] == NULL) {
                            throw new noitpecxe("No Arguments!\n", 990);
                        }
                        if ($args[$arg_val] === "noitpecxe") {
                            throw new noitpecxe("No Exceptions!\n", 100);
                        }
                        $class = new $token[$j];
                        $class($args, $arg_val);
                        $arg_val++;
                    } catch (noitpecxe $e) {
                        echo "Error Executing Code! Error: " . $e . "\n";
                    }
                    
                }
            }
        }
    }

?>