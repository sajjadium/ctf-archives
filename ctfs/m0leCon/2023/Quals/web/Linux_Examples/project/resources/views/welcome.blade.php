<!DOCTYPE html>
<html>
    <head>
        <title>Linux examples</title>
    </head>
    <body>
        <h2>Linux examples</h2>
        <a href="/run?cmd=0">ls -al /</a>
        <br />
        <a href="/run?cmd=1">df -h</a>
        <br />
        <a href="/run?cmd=2">ss -l</a>
        <br />
        <a href="/run?cmd=3">ip a</a>
        <br />
        <a href="/run?cmd=4">ip r</a>
        <br />
        <a href="/run?cmd=5">ps aux</a>
        <br />
        <br />
        You IP is: {{request()->ip()}}
    </body>
</html>
