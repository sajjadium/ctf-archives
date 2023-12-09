<?php
$define_math_constants = fn() =>
define('PI', 3) &&
define('E', 3) &&
define('g', 9);

$instructions = [
    '=' => fn(&$lval, $rval) => $lval = $rval,
    '+=' => fn(&$lval, $rval) => $lval = $lval + $rval,
    '-=' => fn(&$lval, $rval) => $lval = $lval - $rval,
    '*=' => fn(&$lval, $rval) => $lval = $lval * $rval,
    '/=' => fn(&$lval, $rval) => $lval = $lval / $rval,
    '_' => fn(&$lval, $rval) => $lval = $lval,
];

$check_lval = fn($lval) => $lval[0] == '$' && ctype_graph(substr($lval, 1));

$check_rval = fn($rval) => $check_lval($rval) || ctype_digit($rval) || ctype_alpha($rval);

// Instruction as quadruple
// (name, [lval, rval], deps, deref_rval)
$parse_instruction = fn($i) =>
    (strlen($i) == 0 || ($i[0] == '#') ? // Comments
    []
    : (
        // Remove whitespaces
        ($i = preg_replace('/\s\s+/', ' ', $i)) &&
        ($i = trim($i)) &&
        (strpos($i, "FLAG") === false) &&
        // Explode Instruction
        ($instr_splitted = explode(" ", $i, 3)) &&
        // Parse
        (count($instr_splitted) == 3) &&
        ([$lval, $op, $rval] = $instr_splitted) &&
        $check_lval($lval) &&
        // Remove reference
        ($lval = substr($lval, 1)) &&
        $check_rval($rval) &&
        array_key_exists($op, $instructions) ?
        // Instruction is ok, check if deref is needed
        (
            ctype_digit($rval) ||
            ctype_alpha($rval) ||
            // Remove leading $
            (($rval = substr($rval, 1)) && false) ?
            [$op, [$lval, $rval], [$lval], false]
            : [$op, [$lval, $rval], [$lval, $rval], true]
        )
        : []// Instruction not found
    )
);

$parse_number = fn($num) =>
    (
    $num != '' &&
    ($num = trim($num)) &&
    ctype_digit($num) ?
    intval($num)
    : (defined($num) && $num != "FLAG" ?
        constant($num)
        : 0
    )
);

$execute_pipeline = function (&$mysqli) {
    global $constants;
    global $instructions;
    $pipeline = $_SESSION['pipeline'];

    try {
        global $x;
        $x = $pipeline['num'];
        foreach ($pipeline['instructions'] as $instr) {

            if ($instr == []) {
                continue;
            }

            [$op, $args, $deps, $deref] = $instr;

            // Fix scoping
            foreach ($deps as $d) {
                global ${$d};
                if (!isset($$d)) {
                    $$d = 0;
                }

            }
            [$lval, $rval] = $args;

            // Constants
            if (!$deref && ctype_alpha($rval)) {
                $rval = constant($rval);
            }

            if ($deref) {
                $rval = $$rval;
            }
            $instructions[$op]($$lval, $rval);
        }
        $stmt = $mysqli->prepare('UPDATE numbers SET num = ?, processed = 1, processed_date = NOW() WHERE id = ?');
        $stmt->bind_param("si", $x, $pipeline['id']);
        $res = $stmt->execute();
        set_user_hook('pipeline_success');
    } catch (Exception $e) {
        set_user_hook('pipeline_failure');
    } catch (Error $e) {
        set_user_hook('pipeline_failure');
    }
};

$router_global_methods = [
    'parse_instruction',
    'parse_number',
];
$router_global_vars = [
];

// Register global variables for the router
if (isset($register_global)) {
    foreach ($router_global_methods as $method) {
        $register_global($method);
    }

    foreach ($router_global_vars as $var) {
        $register_global($var);
    }

}

register_init_hook($define_math_constants);

// Register possible user hooks
register_new_user_hook('start_processing', $execute_pipeline, [ &$mysqli]);
