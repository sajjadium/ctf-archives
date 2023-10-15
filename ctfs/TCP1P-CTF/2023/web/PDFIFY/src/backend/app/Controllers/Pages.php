<?php

namespace App\Controllers;

helper("render");

class Pages extends BaseController
{
    public function home()
    {
        return (new \Template('pages/home'))
            ->setData('title', 'Home')
            ->render();
    }
    public function register()
    {
        return (new \Template('pages/register'))
            ->setData('title', 'Register')
            ->render();
    }
    public function login()
    {
        return (new \Template('pages/login'))
            ->setData('title', 'Login')
            ->render();
    }
}
