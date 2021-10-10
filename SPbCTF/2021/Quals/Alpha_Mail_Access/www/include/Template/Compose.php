<?php
class Template_Compose extends Template {
    protected $template = <<<TEMPLATE_END
<h1>.compose</h1>
<a href="/inbox">&laquo; Back to Manly Inbox</a><p/>
<form method="POST">
<table border="0" cellpadding="2">
<tr><td align="right">To</td><td align="left"><input type="text" name="to" value="{to}" size="26" /></td></tr>
<tr><td align="right">Subject</td><td align="left"><input type="text" name="subject" value="{subject}" size="26" /></td></tr>
<tr><td colspan="2" align="center"><textarea name="body" cols="35" rows="10">
{mail_body}</textarea></td></tr>
<tr><td colspan="2" align="center"><input type="submit" value="Send" /></td></tr>
</table>
</form>
<br/>
{send_result}
TEMPLATE_END;
}
