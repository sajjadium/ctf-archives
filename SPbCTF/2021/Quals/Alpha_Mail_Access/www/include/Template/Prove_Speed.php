<?php
class Template_Prove_Speed extends Template {
    protected $template = <<<TEMPLATE_END
<h1>.prove.speed</h1>
<div class='method-speed'>Speed</div>
<a href="/prove">&laquo; Back to Methods</a><p/>
As a real man, you need to be fast<br/>
enough to enter hundred pictures<br/>
in three minutes:<br/>
<img src="/captcha" />
<form method="POST" action="/prove/speed/{number}">
    <input type="text" name="captcha" size="10" autofocus="autofocus" /> <input type="submit" value="Check" />
</form>
<p/>
First: {first}<br/>
Last: {last}<br/>
Correct: {number}<p/>
{message}
TEMPLATE_END;
}
