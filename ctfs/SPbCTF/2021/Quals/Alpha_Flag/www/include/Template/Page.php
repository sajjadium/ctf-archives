<?php
class Template_Page extends Template {
    protected $template = <<<TEMPLATE_END
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>{title} :: Alpha Mail</title>
        <link rel="stylesheet" href="/static/css/style.css" type="text/css" />
        {head}
    </head>
    <body>
        <center><table border="0">
            <tr><td class="logo"></td><td class="brand">Alpha Mail<div>Postal Service for Real Machos</div></td></tr>
            <tr>
                <td class="menu" valign="top">{menu}</td>
                <td class="body" valign="top" align="center">{body}</td>
            </tr>
        </table></center>
    </body>
</html>
TEMPLATE_END;
}
