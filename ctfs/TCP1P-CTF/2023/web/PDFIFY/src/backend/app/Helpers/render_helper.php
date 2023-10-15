<?php

class Template
{
    protected $name;
    protected $data;

    function __construct($name = "")
    {
        $this->name = $name;
        $this->data = array();
        $this->data['title'] = "default-title";
    }
    function __toString()
    {
        return view("templates/header", $this->data)
            . view($this->name)
            . view("templates/footer");
    }
    public function setData($key, $value)
    {
        $this->data[$key] = $value;
        return $this;
    }
    public function render()
    {
        return view('templates/header', $this->data)
            . view($this->name)
            . view('templates/footer');
    }
}
