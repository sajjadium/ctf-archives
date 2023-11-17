<html>
    <head>
        <title>Smarty Pants</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    </head>
    <body class="container mt-4">
        {if isset($error) }
            <div class="alert alert-danger" role="alert">
            <strong>ERROR:</strong> {$error}
            </div>
        {/if}
        <p>You want the flag?</p>
        <p>You must beat my regex filter first <code>{$pattern}</code></p>
        <p>Smarty Version: {$smarty.version}</p>
        <form method="post">
            <div class="mb-3">
                <label for="data" class="form-label">Template:</label>
                <textarea class="form-control" rows="6" id="data" name="data"></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        <p><a href="/?source">view source</a></p>
    </body>
</html>
