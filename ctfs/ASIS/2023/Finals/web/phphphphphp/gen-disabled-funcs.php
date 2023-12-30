<?php
$blocked = ["header_register_callback", "getenv", "putenv", "error_log", "error_get_last", "error_clear_last", "register_shutdown_function", "ini_get", "ini_get_all", "ini_set", "ini_alter", "ini_restore", "ini_parse_quantity", "set_include_path", "register_tick_function", "unregister_tick_function","parse_ini_file", "parse_ini_string", "openlog", "closelog", "syslog", "assert", "assert_options", "exec", "system", "passthru", "shell_exec", "proc_nice", "pclose", "popen", "rmdir", "realpath", "sys_get_temp_dir", "fsockopen", "pfsockopen", "readlink", "linkinfo", "symlink", "link", "mail", "proc_open", "proc_close", "proc_terminate", "proc_get_status"];

$exts = get_loaded_extensions();
foreach($exts as $ext){
	if($ext != 'standard'){
		$funcs = get_extension_funcs($ext);		
		if($funcs == null) continue;
		$blocked = array_merge($funcs,$blocked);
	}
}
echo implode(',',$blocked)."\n";

