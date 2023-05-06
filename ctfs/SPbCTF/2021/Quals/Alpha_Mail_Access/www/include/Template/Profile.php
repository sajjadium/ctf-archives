<?php
class Template_Profile extends Template {
    protected $template = <<<TEMPLATE_END
<h1>.profile</h1>
Real men don't change their mind, but:<p/>
<form method="POST">
<table border="0" cellpadding="2">
<tr><td align="right">Login</td><td align="left"><input type="text" readonly="readonly" value="{login}" /></td></tr>
<tr><td align="right">Password</td><td align="left"><input type="password" name="password" /></td></tr>
<tr><td align="right">Proven</td><td align="left"><input type="text" readonly="readonly" value="{proven}" /></td></tr>
{profile}
<tr><td colspan="2" align="center"><input type="submit" value="Update" /></td></tr>
</table>
</form>
<br/>
{profile_result}
TEMPLATE_END;
}
