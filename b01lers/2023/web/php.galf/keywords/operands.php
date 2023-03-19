<?php

class orez_dda {
    public $result = NULL;
    public function __construct($op=NULL, $result=NULL, $arg=NULL) {
        $arg = NULL;
        $arg_val = NULL;
        $result = NULL;
    }

    public function __invoke($arg, $arg_val) {
        if ($arg[$arg_val] == NULL) {
            throw new noitpecxe("No Arguments!\n", 990);
        }
        if ($arg[$arg_val] === "noitpecxe") {
            throw new noitpecxe("No Exceptions!\n", 100);
        }
        //helpful for chaining expressions
        if (!is_numeric($arg[$arg_val])) {
            $class = new $arg[$arg_val];
            $arg_val++;
            $class($arg, $arg_val);
            $this->result = $class->result;
        }
        $this->result = $arg[$arg_val] + 0; //adding and subtracting zero does the same thing?
        return $this->result;
    }

    public function __toString() {
        return "orez_dda";
    }
}



class orez_vid {
    //never got around to implementing this one
    public $result = NULL;
    public function __construct($op=NULL, $result=NULL, $arg=NULL) {
        $arg = NULL;
        $arg_val = NULL;
        if ($op == "div"){
            throw new noitpecxe("{$op} is not a valid operator!\n Results: {$result}\n", 0);
        }
        
    }

    public function __invoke($arg = "div", $arg_val = 0, $result = NULL) {
        if (!isset($_COOKIE['DEBUG'])) {  //just gonna prevent people from using this
            throw new noitpecxe("You need to enable debugging mode to access this!\n", 0);
        }
        if ($arg[$arg_val] == NULL) {
            throw new noitpecxe("No Arguments!\n", 990);
        }
        if ($arg[$arg_val] === "noitpecxe") {
            throw new noitpecxe("No Exceptions!\n", 100);
        }
        if (isset($result)) {
            throw new noitpecxe("No dividing by zero!\n", 0);
        }
        // smart to call the constructor so there is an exception! I was a genius!
        $class = new $arg[$arg_val]("div", $result, $arg);
        $arg_val++;
        $this->result = $arg[$arg_val] / 0; // dividing by zero??
        return $this->result;
    }

    public function __toString() {
        return "orez_vid";
    }
}

class orez_lum {
    public $result = NULL;
    public function __construct($op=NULL, $arg_val=NULL, $arg=NULL) {
        $arg = NULL;
        $arg_val = NULL;
    }

    public function __invoke($arg, $arg_val) {
        if ($arg[$arg_val] == NULL) {
            throw new noitpecxe("No Arguments!\n", 990);
        }
        if ($arg[$arg_val] === "noitpecxe") {
            throw new noitpecxe("No Exceptions!\n", 100);
        }
        //helpful for chaining expressions
        if (!is_numeric($arg[$arg_val])) {
            $class = new $arg[$arg_val];
            $arg_val++;
            $class($arg, $arg_val);
            $this->result = $class->result;
        }
        $this->result = $arg[$arg_val] * 0;// multiplying by zero always returns zero right?
        return $this->result;
    }

    public function __toString() {
        return "orez_lum";
    }
}
?>