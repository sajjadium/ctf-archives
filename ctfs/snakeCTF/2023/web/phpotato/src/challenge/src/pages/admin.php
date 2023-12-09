<?php
// Page init hooks
register_init_hook($check_auth, [$_SESSION]);
register_init_hook($check_admin, [$_SESSION]);
execute_init_hooks();

// Logic handling
$account_numbers = [
    'unprocessed' => '',
    'processed' => '',
];

$render_number_unprocessed = fn ($x) => $x = "
    <div class='numbers'>
        <form method='POST'>
            <input type='hidden' name='_METHOD' value='POST'>
            <input type='text' name='id' hidden value=" . $x['id'] . " />
            <p class='num'>
                <span>Number: " . (is_numeric($x['num']) ? number_format($x['num'], $precision) : $x['num']) . "</span>
            </p>
            <div class='pipe'>
                <code>
                    Redacted pipeline for safety
                </code>
            </div>
            <div class='actions'>
                <input type='submit' name='submit' value='Process' class='written-submit'></input>
                <input type='submit' name='submit' value='Delete' class='written-submit'></input>
            </div>
        </form>
    </div>
    ";

$render_number_processed = fn ($x) => $x = "
    <div class='numbers'>
        <form method='POST'>
        <input type='hidden' name='_METHOD' value='POST'>
        <input type='text' name='id' hidden value=" . $x['id'] . " />
            <p class='num'>
                <span>Number: " . (is_numeric($x['num']) ? number_format($x['num'], $precision) : $x['num']) . "</span>
                <span>Processed at {$x['processed_date']}</span>
            </p>
            <input type='submit' name='submit' class='written-submit' value='Delete'></input>
        </form>
    </div>
    ";

$handle_get = fn (&$mysqli, &$account_numbers) => ($query = "SELECT * FROM numbers WHERE user_id = " . $_SESSION['id'] . " AND processed = 0") &&
    ($query_result = $mysqli->query($query)) &&
    (
        ($res = $query_result->fetch_all(MYSQLI_ASSOC)) &&
        ($account_numbers['unprocessed'] = implode(array_map($render_number_unprocessed, $res)))
        || true
    ) &&
    ($query = "SELECT * FROM numbers WHERE user_id = " . $_SESSION['id'] . " AND processed = 1") &&
    ($query_result = $mysqli->query($query)) &&
    (
        ($res = $query_result->fetch_all(MYSQLI_ASSOC)) &&
        ($account_numbers['processed'] = implode(array_map($render_number_processed, $res)))
        || true
    );

// Internal routing
$handle_get($mysqli, $account_numbers);

// Render function
$render = fn () => print("
<html>
    <head>
        <title>Admin page</title>
        <link rel='stylesheet' href='assets/main.css'></style>
    </head>
    <body>
        <div class='ruled-paper'>
            <div class='ruled-paper-header'>
                <h1>Add your favorite number and do crypto stuff</h1>
            " . (isset($message) ?
                "<div class='message'>
                    <p>$message</p>
                </div>"
    : '') . "
            </div>
            <div class='ruled-paper-body' >
                <div>
                    <p class='begin-section'>Add</p>
                    <form method='POST'>
                        <input type='hidden' name='_METHOD' value='PUT'>
                        <div class='form-entry written-form-entry'>
                            <label for='name'>Number</label>
                            <input type='text' name='num' class='box-input'></input>
                        </div>
                        <div class='form-entry written-form-entry'>
                            <label for='pipeline'>Pipeline to be executed:</label>
                            <textarea name='pipeline' class='box-input' placeholder='# Add here your code'></textarea>
                        </div>
                        <input type='submit' name='submit' value='Create' class='written-submit'></input>
                    </form>
                </div>
                <div class='number-container'>
                    <p class='begin-section'>Numbers to be processed:</p>
                    {$account_numbers['unprocessed']}
                </div>
                <div>
                    <p class='begin-section'>Numbers processed:</p>
                    {$account_numbers['processed']}
                </div>
            </div>
        </div>
    </body>
</html>");
