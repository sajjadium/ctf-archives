<?php
class Template_Inbox_Mail extends Template {
    protected $template = <<<TEMPLATE_END
<h1>.mail</h1>
<h3>spbctf{...FIRST.FLAG...}</h3>
<a href="/inbox">&laquo; Back to Manly Inbox</a> | <a href="/compose/{id}">Reply</a><p/>
<table border="1" cellpadding="2">
<thead><tr><th>From</th><th>Subject</th><th>Date</th></tr></thead>
{mail_meta}
</table><p/>
{mail_body}
TEMPLATE_END;
}
