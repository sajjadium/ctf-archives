<?php
class Template_Register extends Template {
    protected $template = <<<TEMPLATE_END
<h1>.register</h1>
<form method="POST">
<table border="0" cellpadding="2">
<tr><td align="right">Login</td><td align="left"><input type="text" name="login" /></td></tr>
<tr><td align="right">Password</td><td align="left"><input type="password" name="password" /></td></tr>
<tr><td align="right">Confirm</td><td align="left"><input type="password" name="password2" /></td></tr>
<tr><td colspan="2" align="center"><input type="submit" value="Register" /></td></tr>
</table>
</form>
<br/>
{reg_result}
TEMPLATE_END;
}
