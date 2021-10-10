<?php
class Template_Prove_Stamina extends Template {
    protected $template = <<<TEMPLATE_END
<h1>.prove.stamina</h1>
<div class='method-stamina'>Stamina</div>
<a href="/prove">&laquo; Back to Methods</a><p/>
As a real man, you need to endure<br/>
continuous seven days of clicking:<br/>
<form method="POST" action="/prove/stamina/{number}">
    <input type="submit" value="Click" />
</form>
<p/>
First: {first}<br/>
Last: {last}<p/>
{message}
TEMPLATE_END;
}
