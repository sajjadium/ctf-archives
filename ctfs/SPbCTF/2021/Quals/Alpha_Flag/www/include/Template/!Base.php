<?php
abstract class Template {
    private $vars;
    protected $template;

    function __construct() {
        $this->vars = [];
    }

    function AssignVariable($name, $value) {
        $this->vars[$name] = new Misc_ProfanityFilter($value);
    }

    function AssignVariables($vars) {
        foreach ($vars as $name => $value) {
            $this->AssignVariable($name, new Misc_ProfanityFilter($value));
        }
    }

    function __toString() {
        $vars = $this->vars;
        return preg_replace_callback('/\{(\w+)\}/', function ($m) use ($vars) { return $vars[$m[1]]; }, $this->template);
    }
}
