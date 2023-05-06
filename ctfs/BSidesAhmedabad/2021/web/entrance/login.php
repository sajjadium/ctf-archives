<?php
session_start();

$users = array(
    "admin" => "caa6d4940850705040738b276c7bb3fea1030460",
    "guest" => "35675e68f4b5af7b995d9205ad0fc43842f16450"
);

function lookup($username) {
    global $users;
    return array_key_exists($username, $users) ? $users[$username] : "";
}

if (!empty($_POST['username']) && !empty($_POST['password'])) {
    $sha1pass = lookup($_POST['username']);
    if ($sha1pass == sha1($_POST['password'])) {
        $_SESSION['login'] = true;
        $_SESSION['privilege'] = $_POST['username'] == "guest" ? "guest" : "admin";
        header("Location: /");
        exit();
    } else {
        $fail = true;
    }
}
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Entrance</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/uikit@3.7.6/dist/css/uikit.min.css" />
        <script src="https://cdn.jsdelivr.net/npm/uikit@3.7.6/dist/js/uikit.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/uikit@3.7.6/dist/js/uikit-icons.min.js"></script>
    </head>
    <body class="uk-container">
        <form method="POST" action="/login.php">
            <?php if (isset($fail)) { ?>
                <div class="uk-alert-danger" uk-alert>
                    <a class="uk-alert-close" uk-close></a>
                    <p>Invalid username or password</p>
                </div>
            <?php } ?>
            <div class="uk-section uk-section-muted uk-flex uk-flex-middle uk-animation-fade" uk-height-viewport>
                <div class="uk-width-1-1">
                    <div class="uk-container">
                        <div class="uk-grid-margin uk-grid uk-grid-stack" uk-grid>
                            <div class="uk-width-1-1@m">
                                <div class="uk-margin uk-width-large uk-margin-auto uk-card uk-card-default uk-card-body uk-box-shadow-large">
                                    <h3 class="uk-card-title uk-text-center">Welcome!</h3>
                                    <form>
                                        <div class="uk-margin">
                                            <div class="uk-inline uk-width-1-1">
                                                <span class="uk-form-icon" uk-icon="icon: user"></span>
                                                <input class="uk-input uk-form-large" type="text" name="username">
                                            </div>
                                        </div>
                                        <div class="uk-margin">
                                            <div class="uk-inline uk-width-1-1">
                                                <span class="uk-form-icon" uk-icon="icon: lock"></span>
                                                <input class="uk-input uk-form-large" type="password" name="password">
                                            </div>
                                        </div>
                                        <div class="uk-margin">
                                            <button class="uk-button uk-button-primary uk-button-large uk-width-1-1">Login</button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </body>
</html>
