<?php
class Template_Inbox_List extends Template {
    protected $template = <<<TEMPLATE_END
<h1>.inbox</h1>
<table border="1" cellpadding="2">
<thead><tr><th>From</th><th>Subject</th><th>Date</th></tr></thead>
{inbox_list}
</table>
TEMPLATE_END;
}
