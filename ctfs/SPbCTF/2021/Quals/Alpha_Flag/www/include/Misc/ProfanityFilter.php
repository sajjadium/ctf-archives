<?php
class Misc_ProfanityFilter {
    private $str;

    function __construct($str) {
        $this->str = $str;
    }

    function __toString() {
        $rules = [
            '/cunt/i' => 'c**t',
            '/fuck/i' => 'f**k',
            '/firetruck/i' => 'f********k',
            '/asshole/i' => 'a****le',
            '/bitch/i' => 'b***h',
            '/shit/i' => 's**t',
        ];
        return preg_replace(array_keys($rules), array_values($rules), $this->str);
    }
}
