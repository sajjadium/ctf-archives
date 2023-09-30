<?php

require_once __DIR__ . '/db.php';
$pdo = connectToDatabase();

preg_match('|/m/([^?/]*)(?:/([^?/]*))?/?|', $_SERVER['REQUEST_URI'], $re);
$__BIN_ID = $re[1];
$__REQUEST_ID = $re[2];
if (str_ends_with($__BIN_ID, '/')) {
    $__BIN_ID = substr($__BIN_ID, 0, -1);
}

// Check access
if (!isset($_SESSION['id']) || $_SESSION['id'] !== $__BIN_ID) {
    http_response_code(401);
    die;
}

try {
    $stmt = $pdo->prepare('SELECT * FROM `bin` WHERE `id`=? AND `owner`=?');
    $stmt->execute([$__BIN_ID, $_SESSION['username']]);
    $res = $stmt->fetchall();
    if (count($res) !== 1) {
        http_response_code(401);
        die;
    }
} catch (Exception $e) {
    http_response_code(500);
    die;
}

// Update config
if (isset($_POST['response']) && isset($_POST['headers'])) {
    try {
        if (!$_POST['response']) {
            throw new Exception();
        }
        $data = json_decode($_POST['headers']);
        if ($data === NULL) {
            throw new Exception();
        }
        foreach ($data as $key => $value) {
            if (!is_string($key) || !is_string($value) || !preg_match('/^[A-Za-z0-9-]+$/', $key) || !preg_match('/^[^\r\n]+$/', $value)) {
                throw new Exception();
            }
        }
    } catch (Exception $e) {
        header('Location: ?error');
        die;
    }

    $stmt = $pdo->prepare('UPDATE `bin` SET `response_text`=?, `response_headers`=? WHERE `id` = ?');
    $stmt->execute([$_POST['response'], json_encode(json_decode($_POST['headers'])), $__BIN_ID]);

    if (isset($_GET['error'])) {
        header('Location: /m/' . $__BIN_ID . (!!$__REQUEST_ID ? '/' . $__REQUEST_ID : ''));
        die;
    }
}

// Get bin data
$stmt = $pdo->prepare('SELECT * FROM `bin` WHERE `id`=? AND `owner`=?');
$stmt->execute([$__BIN_ID, $_SESSION['username']]);
$res = $stmt->fetchall();
$__BIN = $res[0];

// Read logs
$logs = [];
if (file_exists(__DIR__ . '/../data/' . $__BIN_ID)) {
    $data = file_get_contents(__DIR__ . '/../data/' . $__BIN_ID);
    $logs = explode("****", $data);
    for ($i = 0; $i < count($logs); $i++) {
        $logs[$i] = json_decode(base64_decode($logs[$i]));
    }
}
$logs = array_reverse($logs);

$__REQUEST = NULL;

if ($__REQUEST_ID !== NULL) {
    for ($i = 0; $i < count($logs); $i++) {
        if ($logs[$i]->id === $__REQUEST_ID) {
            $__REQUEST = $logs[$i];
            break;
        }
    }
    if ($__REQUEST === NULL) {
        header('Location: /m/' . $__BIN_ID);
        die;
    }
}

// Helper function
function printTable($name, $obj)
{
    $filtered = array_filter((array) $obj, fn ($x) => !!$x);
    if (count($filtered) > 0) {
?>
        <div>
            <h3 style="margin-top: 2.5rem;"><?php echo $name; ?></h3>
            <table>
                <thead>
                    <th>
                        Name
                    </th>
                    <th>
                        Value
                    </th>
                </thead>
                <tbody>
                    <?php
                    foreach ($filtered as $key => $value) {
                    ?>
                        <tr>
                            <td><?php echo $key; ?></td>
                            <td><?php echo $value; ?></td>
                        </tr>
                    <?php
                    }
                    ?>
                </tbody>
            </table>
        </div>
<?php
    }
}

?>

<!DOCTYPE html>
<html lang=" en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/style.css">
    <style>
        #bin-url {
            background: #aaa;
            font-family: 'Source Code Pro', monospace;
            padding: 0.375rem 0.75rem;
            border-radius: 8px;
            border: none;
            margin-left: .35rem;
            /* bg-neutral-800 px-3 py-1.5 rounded-md ml-2 */
        }

        #main {
            display: grid;
            gap: 2rem;
            grid-template-columns: 3fr 7fr;
            margin-top: 2rem;
            margin-bottom: 2rem;
        }

        h2 {
            font-weight: semibold;
            font-size: 1.75rem;
            line-height: 2rem;
        }

        .logs {
            flex: 1 1 0;

            display: flex;
            flex-direction: column;
            gap: .75rem;
            padding: 0;

            height: 100%;
            overflow-y: auto;
        }

        .logs a {
            color: inherit;
            text-decoration: none;
        }

        .log-entry {
            background-color: #ffffff22;
            transition: background-color 75ms ease-in-out;
            list-style: none;
            padding: 1rem 1.75rem;

            border-radius: 8px;

            display: flex;
            align-items: center;
            gap: 1.25rem;

            cursor: pointer;
        }

        .log-entry:hover {
            background-color: #ffffff33;
        }

        .log-entry .date {
            font-size: .75rem;
            font-weight: bold;
            white-space: nowrap;
        }

        .log-entry .method {
            font-weight: bold;
            font-family: 'Source Code Pro', monospace;
            white-space: nowrap;
        }

        .method.GET {
            color: greenyellow;
        }

        .method.DELETE {
            color: orange;
        }

        .method.PUT {
            color: cadetblue;
        }

        .method.POST {
            color: cornflowerblue;
        }

        .method.PATCH {
            color: darksalmon;
        }

        .log-entry .path {
            font-family: 'Source Code Pro', monospace;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }

        thead {
            background-color: rgb(var(--accent-color), .2);
        }

        th,
        td {
            padding: .75rem 1.25rem;
            border: 1px solid #ccc;
            vertical-align: top;
        }

        td:first-child {
            font-weight: bold;
            width: 20%;
        }

        .request-info {
            display: flex;
            font-size: 1.25rem;
            font-weight: bold;
            margin-bottom: -0.5rem;
            gap: 2rem;
        }

        .config-btn {
            cursor: pointer;
            background-color: #FFFFFF40;
            color: white;
            border: none;
            border-radius: 8px;
            padding: .75rem 2rem;
            font-size: 1rem;
            transition: background-color 75ms ease;
        }

        .config-btn:hover {
            background-color: #FFFFFF30;
        }

        dialog {
            width: 90%;
            max-width: 50vw;
            border: none;
            border-radius: 12px;
            padding: 2rem 2.5rem;
        }

        dialog::backdrop {
            background: rgba(0, 0, 0, 0.5);
        }

        dialog label {
            font-weight: bold;
        }

        dialog textarea {
            width: 100%;
            margin: .5rem 0;
            min-height: 4rem;
        }

        dialog button {
            border: none;
            border-radius: 8px;
            padding: .75rem 2rem;
            font-weight: bold;
            cursor: pointer;
            font-size: 1rem;
        }

        dialog button:last-of-type {
            background: var(--accent);
        }

        input[type=checkbox] {
            font-weight: 2rem;
        }

        input[type=checkbox]+label {
            font-weight: normal;
            width: 100%;
            display: block;
            cursor: pointer;
        }

        .checkbox-container {
            margin-top: 1rem;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: .5rem;
        }
    </style>
    <title>TrashBin</title>
</head>

<body class="bg-neutral-800 flex flex-col h-full text-white">

    <header>
        <nav>
            <a href="/">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                </svg>
                <div>
                    TrashBin
                </div>
            </a>

            <div>
                <div>
                    <!-- I tried so hard, but in the end one line of JS was required -->
                    <button class="config-btn" onclick="dialog.showModal()">Configure bin</button>
                </div>
                <div>
                    Bin URL: <input id="bin-url" readonly value="<?php echo 'http://' . $_SERVER['HTTP_HOST'] . '/b/' . $__BIN_ID; ?>">
                </div>
                <div>
                    Welcome, <u><?php echo $_SESSION['username']; ?></u>!
                </div>
            </div>
        </nav>
    </header>

    <section id="main">
        <div class="" style="display: flex; flex-direction: column; max-width: 100%;"">
            <h2 class=" accent">Requests</h2>

            <ul class="logs">
                <?php
                foreach ($logs as $log) {
                ?>
                    <a href="/m/<?php echo $__BIN_ID . '/' . $log->id; ?>">
                        <li class="log-entry">
                            <div class="date"><?php echo date("M d, H:i:s", $log->time); ?></div>
                            <div class="method <?php echo $log->method; ?>"><?php echo $log->method; ?></div>
                            <div class="path"><?php echo $log->raw_path; ?></div>
                        </li>
                    </a>
                <?php
                }
                ?>
            </ul>
        </div>
        <div class="" style="display: flex; flex-direction: column; max-width: 100%;">
            <?php
            if ($__REQUEST_ID === NULL) {
            ?>
                <div style=" width: 100%; height: 80%; display: flex; justify-content: center; align-items: center">
                    <em>You have no request opened. You can configure your TrashBin with the button in the navbar.</em>
                </div>
            <?php
            } else {
            ?>
                <h2 class="accent">Request <?Php echo $__REQUEST_ID; ?></h2>
                <div style=" flex: 1 1 0; height: 100%; overflow-y: auto; padding: 1rem 1rem 1.5rem 0;">
                    <div class="request-info">
                        <div class="method <?php echo $__REQUEST->method; ?>"><?php echo $__REQUEST->method; ?></div>
                        <div><?php echo $__REQUEST->path; ?></div>
                    </div>
                    <?php
                    printTable('Query parameters', $__REQUEST->query);
                    printTable('Headers', $__REQUEST->headers);
                    printTable('Cookies', $__REQUEST->cookies);
                    printTable('Form data', $__REQUEST->form);

                    if (!!$__REQUEST->raw_body) {
                    ?>
                        <div>
                            <h3 style="margin-top: 2.5rem;">Raw body</h3>
                            <pre style="text-align: left;"><code style="text-align: left;"><?php echo $__REQUEST->raw_body; ?></code></pre>
                        </div>
                    <?php
                    }
                    ?>
                </div>
            <?php
            }
            ?>
        </div>
    </section>


    <dialog id="dialog">
        <h2 style="margin-bottom: 1rem; font-weight: bold;">Bin configuration</h2>
        <p>Here you can configure how your bin behaves when it receives a request.</p>
        <p>You can use templates to include dynamic data from get parameters/headers/cookies/form parameters. You can access this data with the following format: ${GET[name]}.</p>
        <form method="post">
            <div>
                <label for="response">Bin reponse</label>
            </div>
            <div>
                <textarea id="response" name="response" required><?php echo $__BIN['response_text']; ?></textarea>
            </div>
            <div>
                <label for="headers">Headers</label>
            </div>
            <div>
                <textarea id="headers" name="headers" required><?php echo json_encode(json_decode($__BIN['response_headers']), JSON_PRETTY_PRINT); ?></textarea>
            </div>
            <div style="margin-top: -.5rem; margin-bottom: .5rem; <?php if (isset($_GET['error'])) echo 'color:red;'; ?>"><small>Please use a JSON with string keys and values for headers. Something like {"X-Custom-Header": "value"}</small></div>
            <div class="checkbox-container">
                <input type="checkbox" <?php if ($_SESSION['demo']) echo 'disabled'; ?> id="trigger_request"><label for="trigger_request">Trigger request to external endpoint. Enable to configure.</label>
            </div>
            <div style="margin-bottom: .5rem; color:red;"><small>This feature is only available to premium users with paid plans. This has definitely nothing to do with challenge deadlines.</small></div>
            <div style="margin-top: 2rem; text-align: right;">
                <button value=" cancel" formmethod="dialog">Cancel</button>
                <button id="confirmBtn" value="default">Save</button>
            </div>
        </form>
    </dialog>

    <?php
    if (isset($_GET['error'])) {
    ?>
        <!-- I tried so hard, but in the end one line of JS was required -->
        <script>
            dialog.showModal()
        </script>
    <?php
    }
    ?>

</body>

</html>