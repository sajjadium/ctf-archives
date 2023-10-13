<?php

namespace GadgetOne {
    class Adders
    {
        private $x;
        function __construct($x)
        {
            $this->x = $x;
        }
        function get_x()
        {
            return $this->x;
        }
    }
}
