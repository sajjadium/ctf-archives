<?php
include_once("functions.php");
include_once("config.php");

$result = ['result' => '', 'error' => ''];

if (isset($_SESSION['CSRFToken']) && isset($_POST['csrf_token']) && $_SESSION['CSRFToken'] === $_POST['csrf_token']) {
    if (isset($_SESSION['is_auth']) && $_SESSION['is_auth']) {
        if (isset($_POST['action'])) {

            switch ($_POST['action']) {
                case 'show':
                    $query = db::prepare("SELECT password FROM vault where id=%s", $_POST['id']);
                    $res = db::commit($query);
                    if ($res->num_rows == 1) {
                        $row = $res->fetch_assoc();
                        $result['result'] = $row['password'];
                    }

                    echo json_encode($result);
                    break;

                case 'add':
                    $result['error'] = 'Not Implemented yet.';
                    echo json_encode($result);
                    break;

                default:
                    $result['error'] = 'Undefined action.';
                    echo json_encode($result);
                    break;
            }
        }
    }
    else {
        $result['error'] = 'not authorized';
        echo json_encode($result);
    }
}
else {
    if (isset($_POST['csrf_token'])){
            $result['error'] = "CSRFToken '" . ms($_POST['csrf_token']) . "' is not correct.";  
    }
    else{
        $result['error'] = "No CSRFToken sent.";
    }
    echo json_encode($result);
}

?>

 

