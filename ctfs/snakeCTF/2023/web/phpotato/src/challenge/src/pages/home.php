<?php
// Page init hooks
register_init_hook($check_auth, [$_SESSION]);
execute_init_hooks();

// Logic handling
$account_numbers;
$render_number = fn($x) => $x = "
    <div class='numbers'>
        <p class='num'>
            <span>Number: " . (is_numeric($x['num']) ? number_format($x['num'], $precision) : $x['num']) . "</span>
            <span>Process status: {$x['processed']}
            " . ($x['processed'] ? " @ " . $x['processed_date'] : "")
    . "
            </span>
        </p>
        <div class='pipe'>
            <p>Pipeline:</p>
            <code>
                {$x['pipeline']}
            </code>
        </div>
    </div>
    <hr>";

/* FOR INTERNAL TEST ONLY
$handle_post = fn(&$mysqli) =>
($_SESSION['admin'] ?
($stmt = $mysqli->prepare('UPDATE users SET is_admin = 0 WHERE id = ?'))
: ($stmt = $mysqli->prepare('UPDATE users SET is_admin = 1 WHERE id = ?'))
) &&
$stmt->bind_param("i", $_SESSION['id']) &&
($res = $stmt->execute() ?
(($_SESSION['admin'] = $_SESSION['admin'] != 1) ?
set_user_hook('greet_admin') || true
: true
) &&
header("Refresh:0") ||
exit()
: set_user_hook('something_wrong') ||
header("Refresh:0") ||
exit()
);
 */

$handle_get = fn(&$mysqli, &$account_numbers) =>
    ($query = "SELECT * FROM numbers WHERE user_id = " . $_SESSION['id']) &&
    (isset($_GET['sort']) ?
    ($query .= " ORDER BY processed_date " . $_GET['sort'])
    : true
) &&
    (isset($_GET['limit']) ?
    ($query .= " LIMIT " . $_GET['limit'])
    : true
) &&
    ($query_result = $mysqli->query($query)) &&
    ($res = $query_result->fetch_all(MYSQLI_ASSOC)) &&
    ($account_numbers = implode(array_map($render_number, $res))
);

// Internal routing
//if (isset($_POST['submit'])) {
//    $handle_post($mysqli);
//} else {
$handle_get($mysqli, $account_numbers);
//}

// Render function
$render = fn() => print("
<html>
    <head>
        <title>Welcome {$_SESSION['username']}</title>
        <link rel='stylesheet' href='assets/main.css'></style>
    </head>
    <body>        
        <div class='ruled-paper'>
            <div class='ruled-paper-header'>
                <h1>Let's have some fun</h1>
                " . (isset($message) ? 
                    "<div class='message'>
                        <p>$message</p>
                    </div>"
                     : '') . "
            </div>
            <div class='ruled-paper-body' >
                <div>
                    $account_numbers
                </div>" . "
            </div>
        </div>
    </body>
</html>");
