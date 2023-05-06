<?php
class Template_Main extends Template {
    protected $template = <<<TEMPLATE_END
<h1>.hello</h1>
This is a postal service for real men.<br/><br/>
To join, you need to prove you're a real<br/>macho and not a whining man-child.<p/>
Your options:
<ul>
    <li><a href="/register">Register</a> and <a href="/prove">Prove</a> to be one</li>
    <li><a href="/login">Login</a></li>
    <li><a href="https://www.babytv.com/">Go away</a></li>
</ul>
TEMPLATE_END;
}
