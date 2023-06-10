<?php
    ini_set('display_errors', 0);
    
    $flag =  "SEE{FAKE_FLAG}"; // Oops, my dog ate my flag...

    if (isset($_GET['flag']) && preg_match("/^SEE{.*}$/", $_GET['flag'])) {
        $flag = $_GET['flag'];

        if (isset($_GET['debug']) && isset($_GET['config'])) {
            foreach ($_GET['config'] as $key => $value) {
                ini_set($key, $value);
            }
        }
    }
    
    assert(preg_match("/^SEE{.*}$/", $flag), NULL);
?>

<html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
        <style>
            body {
                background-color: <?php echo $_GET["backgroundColor"] ?>;
                color: <?php echo $_GET["textColor"] ?>
            }
        </style>
    </head>
    <body>
        <div class="d-flex align-items-center min-vh-100">
            <div class="container text-center">
                <h1>Sourceful Guessless Web</h1>
                <div>
                    <p class="lead"> Personalize your flag: 🚩 <?php echo preg_replace("/SEE{(.*)}/", "SEE{********}", $flag); ?></p>
                    <p><i>This site is currently in alpha. The full flag will be available in 2024.</i></p>
                    <form>
                        <div class="form-group row my-2">
                            <label for="backgroundColor" class="col-sm-2 col-form-label">Background Color</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="backgroundColor" name="backgroundColor" placeholder="black">
                            </div>
                        </div>
                        <div class="form-group row my-2">
                            <label for="textColor" class="col-sm-2 col-form-label">Text Color</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="textColor" name="textColor" placeholder="white">
                            </div>
                        </div>
                        <div class="form-group row my-2">
                            <label for="flag" class="col-sm-2 col-form-label">Flag</label>
                            <div class="col-sm-10">
                                <input type="text" class="form-control" id="flag" name="flag" placeholder="SEE{...}">
                            </div>
                        </div>
                        <input hidden name="debug" value="0">
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </body>
</html>