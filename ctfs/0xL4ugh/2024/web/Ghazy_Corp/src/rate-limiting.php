<?php

// FUNCTION TO PUSH ERROR TO DIE()
function push_error($error)
{
    $dbg = array_shift(debug_backtrace());
    return $dbg["file"].": Line ".$dbg["line"].": ".$error;
}

// CHECK IF OUR CONFIG FILE EXISTS/ IF NOT, EXIT THE SCRIPT
if (!(file_exists("rate_limit_config.json")))
{
    die(push_error("No config file found! Looking for \"rate_limit_config.json\"."));
}

// GET CONTENTS OF OUR CONFIG FILE
try
{
    $config = file_get_contents("rate_limit_config.json");
}
catch(Exception $f)
{
    die(push_error("Cannot open file! Looking for \"rate_limit_config.json\". Invalid permissions?"));
}

// PARSE CONFIG FILE
$config = json_decode($config, TRUE);
$config = $config[0];

// ESTABLISH DB FILE NAME
$dbFileName = $config["database_file_name"];

// CHECK IF FILE EXISTS
if (!(file_exists($dbFileName)))
{
    try
    {
        fopen($dbFileName, "w");
    }
    catch(Exception $f)
    {
        die(push_error("Database file \"$dbFileName\" could not be created! invalid permissions?"));
    }
}

// HOIST A VAR TO CARRY DATABASE BUFFER
$db = "null";

// CHECK IF DATABASE ISNT EMPTY FILE
$dbIndexable = FALSE;

// IF IT WORKS, $DB IS UTILIZED
try
{
    $fileBuffer = file_get_contents($dbFileName, LOCK_EX);
    if ($fileBuffer != "")
    {
        $dbIndexable = TRUE;
    }
    if ($dbIndexable)
    {
        $db = json_decode($fileBuffer, TRUE);
    }
}
catch(Exception $f)
{
    die(push_error("Cannot open file! Looking for \"$dbFileName\". Invalid permissions?"));
}

// GET TRUE IP
if (!empty($_SERVER['HTTP_CLIENT_IP']))
{
    $ip = $_SERVER['HTTP_CLIENT_IP'];
}

elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR']))
{
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
}
else
{
    $ip = $_SERVER['REMOTE_ADDR'];
}

// CREATE NEW DB VAR
$newDb = array();

// SORT/REPLACE DATABASE
if ($dbIndexable)
{
    // ITERATE OVER DATABASE
    foreach ($db as $value)
    {
        $timeDiff = time() - $config["interval_time_seconds"];
        // IF TIME OF REQUEST IS WITHIN OUR WINDOW, APPEND TO OUR NEW LIST
        if (strtotime($value["time"]) > $timeDiff)
        {
            array_push($newDb, $value);
        }
        // ELSE DROP THE COLUMN
    }
}

// PUSH THIS REQUEST TO NEW DB
array_push($newDb, array("ip" => $ip, "time" => date("Y-m-d H:i:s"), "user-agent" => $_SERVER['HTTP_USER_AGENT'])); 

//SAVE THE DATABASE
file_put_contents($dbFileName, json_encode($newDb));

if ($dbIndexable)
{
    // RATE LIMITING
    foreach ($newDb as $id)
    {
        // FOR EACH LINE IN $uniqueIds: compare with each line to chack lfor amount of requests in our db from x seconds time.
        $hits = 0;
        foreach ($newDb as $id_1)
        {
            if ($id_1["ip"] == $id["ip"])//&& $id["user-agent"] == $id_1["user-agent"])
            {
                $hits++;
            }
        }
        // IF THEY EXCEED OUR RATE THEN die() or redirect:
        if ($hits >= $config["request_allowance"])
        {
            if ($config['die_on_rate_limit'])
            {
                die("You are being rate-limited!");
            }
            //ELSE:
            header('Location: '.$config['redirect_location']);
        }
    }
}

// VIOLA! The rest of your page goes below:

?>
