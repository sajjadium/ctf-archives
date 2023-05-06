<?php
class Template_Login extends Template {
    protected $template = <<<TEMPLATE_END
<h1>.login</h1>
Remember your shit, man?<p/>
<form method="POST">
<table border="0" cellpadding="2">
<tr><td align="right">Login</td><td align="left"><input type="text" name="login" /></td></tr>
<tr><td align="right">Password</td><td align="left"><input type="password" name="password" /></td></tr>
<tr><td colspan="2" align="center"><input type="submit" value="Login" /></td></tr>
</table>
</form>
<br/>
{login_result}
TEMPLATE_END;
}
