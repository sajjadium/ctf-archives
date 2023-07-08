<?php
	// File Upload Helper class.  Combines some useful functions from FlexForms and FlexForms Modules.
	// (C) 2021 CubicleSoft.  All Rights Reserved.

	class FileUploadHelper
	{
		// Copy included for class self-containment.
		// Makes an input filename safe for use.
		// Allows a very limited number of characters through.
		public static function FilenameSafe($filename)
		{
			return preg_replace('/\s+/', "-", trim(trim(preg_replace('/[^A-Za-z0-9_.\-]/', " ", $filename), ".")));
		}

		public static function NormalizeFiles($key)
		{
			$result = array();
			if (isset($_FILES) && is_array($_FILES) && isset($_FILES[$key]) && is_array($_FILES[$key]))
			{
				$currfiles = $_FILES[$key];

				if (isset($currfiles["name"]) && isset($currfiles["type"]) && isset($currfiles["tmp_name"]) && isset($currfiles["error"]) && isset($currfiles["size"]))
				{
					if (is_string($currfiles["name"]))
					{
						$currfiles["name"] = array($currfiles["name"]);
						$currfiles["type"] = array($currfiles["type"]);
						$currfiles["tmp_name"] = array($currfiles["tmp_name"]);
						$currfiles["error"] = array($currfiles["error"]);
						$currfiles["size"] = array($currfiles["size"]);
					}

					$y = count($currfiles["name"]);
					for ($x = 0; $x < $y; $x++)
					{
						if ($currfiles["error"][$x] != 0)
						{
							switch ($currfiles["error"][$x])
							{
								case 1:  $msg = "The uploaded file exceeds the 'upload_max_filesize' directive in 'php.ini'.";  $code = "upload_err_ini_size";  break;
								case 2:  $msg = "The uploaded file exceeds the 'MAX_FILE_SIZE' directive that was specified in the submitted form.";  $code = "upload_err_form_size";  break;
								case 3:  $msg = "The uploaded file was only partially uploaded.";  $code = "upload_err_partial";  break;
								case 4:  $msg = "No file was uploaded.";  $code = "upload_err_no_file";  break;
								case 6:  $msg = "The configured temporary folder on the server is missing.";  $code = "upload_err_no_tmp_dir";  break;
								case 7:  $msg = "Unable to write the temporary file to disk.  The server is out of disk space, incorrectly configured, or experiencing hardware issues.";  $code = "upload_err_cant_write";  break;
								case 8:  $msg = "A PHP extension stopped the upload.";  $code = "upload_err_extension";  break;
								default:  $msg = "An unknown error occurred.";  $code = "upload_err_unknown";  break;
							}

							$entry = array(
								"success" => false,
								"error" => self::FHTranslate($msg),
								"errorcode" => $code
							);
						}
						else if (!is_uploaded_file($currfiles["tmp_name"][$x]))
						{
							$entry = array(
								"success" => false,
								"error" => self::FHTranslate("The specified input filename was not uploaded to this server."),
								"errorcode" => "invalid_input_filename"
							);
						}
						else
						{
							$currfiles["name"][$x] = self::FilenameSafe($currfiles["name"][$x]);
							$pos = strrpos($currfiles["name"][$x], ".");
							$fileext = ($pos !== false ? (string)substr($currfiles["name"][$x], $pos + 1) : "");

							$entry = array(
								"success" => true,
								"file" => $currfiles["tmp_name"][$x],
								"name" => $currfiles["name"][$x],
								"ext" => $fileext,
								"type" => $currfiles["type"][$x],
								"size" => $currfiles["size"][$x]
							);
						}

						$result[] = $entry;
					}
				}
			}

			return $result;
		}

		public static function GetMaxUploadFileSize()
		{
			$maxpostsize = floor(self::ConvertUserStrToBytes(ini_get("post_max_size")) * 3 / 4);
			if ($maxpostsize > 4096)  $maxpostsize -= 4096;

			$maxuploadsize = self::ConvertUserStrToBytes(ini_get("upload_max_filesize"));
			if ($maxuploadsize < 1)  $maxuploadsize = ($maxpostsize < 1 ? -1 : $maxpostsize);

			return ($maxpostsize < 1 ? $maxuploadsize : min($maxpostsize, $maxuploadsize));
		}

		// Copy included for class self-containment.
		public static function ConvertUserStrToBytes($str)
		{
			$str = trim($str);
			$num = (double)$str;
			if (strtoupper(substr($str, -1)) == "B")  $str = substr($str, 0, -1);
			switch (strtoupper(substr($str, -1)))
			{
				case "P":  $num *= 1024;
				case "T":  $num *= 1024;
				case "G":  $num *= 1024;
				case "M":  $num *= 1024;
				case "K":  $num *= 1024;
			}

			return $num;
		}

		public static function GetChunkFilename()
		{
			if (isset($_SERVER["HTTP_CONTENT_DISPOSITION"]))
			{
				// Content-Disposition: attachment; filename="urlencodedstr"
				$str = $_SERVER["HTTP_CONTENT_DISPOSITION"];
				if (strtolower(substr($str, 0, 11)) === "attachment;")
				{
					$pos = strpos($str, "\"", 11);
					$pos2 = strrpos($str, "\"");

					if ($pos !== false && $pos2 !== false && $pos < $pos2)
					{
						$str = self::FilenameSafe(rawurldecode(substr($str, $pos + 1, $pos2 - $pos - 1)));

						if ($str !== "")  return $str;
					}
				}
			}

			return false;
		}

		public static function GetFileStartPosition()
		{
			if (isset($_SERVER["HTTP_CONTENT_RANGE"]) || isset($_SERVER["HTTP_RANGE"]))
			{
				// Content-Range: bytes (*|integer-integer)/(*|integer-integer)
				$vals = explode(" ", preg_replace('/\s+/', " ", str_replace(",", "", (isset($_SERVER["HTTP_CONTENT_RANGE"]) ? $_SERVER["HTTP_CONTENT_RANGE"] : $_SERVER["HTTP_RANGE"]))));
				if (count($vals) === 2 && strtolower($vals[0]) === "bytes")
				{
					$vals = explode("/", trim($vals[1]));
					if (count($vals) === 2)
					{
						$vals = explode("-", trim($vals[0]));

						if (count($vals) === 2)  return (double)$vals[0];
					}
				}
			}

			return 0;
		}

		public static function HandleUpload($filekey, $options = array())
		{
			if (!isset($_REQUEST["fileuploader"]) && !isset($_POST["fileuploader"]))  return array("success" => false, "error" => "No upload or missing 'fileuploader'.", "errorcode" => "no_upload");

			if (isset($options["allowed_exts"]))
			{
				$allowedexts = array();

				if (is_string($options["allowed_exts"]))  $options["allowed_exts"] = explode(",", $options["allowed_exts"]);

				foreach ($options["allowed_exts"] as $ext)
				{
					$ext = strtolower(trim(trim($ext), "."));
					if ($ext !== "")  $allowedexts[$ext] = true;
				}
			}

			$files = self::NormalizeFiles($filekey);
			if (!isset($files[0]))  $result = array("success" => false, "error" => self::FHTranslate("File data was submitted but is missing."), "errorcode" => "bad_input");
			else if (!$files[0]["success"])  $result = $files[0];
			else if (isset($options["allowed_exts"]) && !isset($allowedexts[strtolower($files[0]["ext"])]))
			{
				$result = array(
					"success" => false,
					"error" => self::FHTranslate("Invalid file extension.  Must be one of %s.", "'." . implode("', '.", array_keys($allowedexts)) . "'"),
					"errorcode" => "invalid_file_ext"
				);
			}
			else
			{
				// For chunked file uploads, get the current filename and starting position from the incoming headers.
				$name = self::GetChunkFilename();
				if ($name !== false)
				{
					$startpos = self::GetFileStartPosition();

					$name = substr($name, 0, -(strlen($files[0]["ext"]) + 1));

					if (isset($options["filename_callback"]) && is_callable($options["filename_callback"]))  $filename = call_user_func_array($options["filename_callback"], array($name, strtolower($files[0]["ext"]), $files[0]));
					else if (isset($options["filename"]))  $filename = (isset($options["fixed_filename"]) && $options["fixed_filename"] ? $options["filename"] : str_replace(array("{name}", "{ext}"), array($name, strtolower($files[0]["ext"])), $options["filename"]));
					else  $filename = false;

					if (!is_string($filename))  $result = array("success" => false, "error" => self::FHTranslate("The server did not set a valid filename."), "errorcode" => "invalid_filename");
					else if (isset($options["limit"]) && $options["limit"] > -1 && $startpos + filesize($files[0]["file"]) > $options["limit"])  $result = array("success" => false, "error" => self::FHTranslate("The server file size limit was exceeded."), "errorcode" => "file_too_large");
					else
					{
						if (file_exists($filename) && $startpos === filesize($filename))  $fp = @fopen($filename, "ab");
						else
						{
							$fp = @fopen($filename, ($startpos > 0 && file_exists($filename) ? "r+b" : "wb"));
							if ($fp !== false)  @fseek($fp, $startpos, SEEK_SET);
						}

						$fp2 = @fopen($files[0]["file"], "rb");

						if ($fp === false)  $result = array("success" => false, "error" => self::FHTranslate("Unable to open a required file for writing."), "errorcode" => "open_failed", "info" => $filename);
						else if ($fp2 === false)  $result = array("success" => false, "error" => self::FHTranslate("Unable to open a required file for reading."), "errorcode" => "open_failed", "info" => $files[0]["file"]);
						else
						{
							do
							{
								$data2 = @fread($fp2, 1048576);
								if ($data2 == "")  break;

								@fwrite($fp, $data2);
							} while (1);

							fclose($fp2);
							fclose($fp);

							$result = array(
								"success" => true
							);
						}
					}
				}
				else
				{
					$name = substr($files[0]["name"], 0, -(strlen($files[0]["ext"]) + 1));

					if (isset($options["filename_callback"]) && is_callable($options["filename_callback"]))  $filename = call_user_func_array($options["filename_callback"], array($name, strtolower($files[0]["ext"]), $files[0]));
					else if (isset($options["filename"]))  $filename = (isset($options["fixed_filename"]) && $options["fixed_filename"] ? $options["filename"] : str_replace(array("{name}", "{ext}"), array($name, strtolower($files[0]["ext"])), $options["filename"]));
					else  $filename = false;

					if (!is_string($filename))  $result = array("success" => false, "error" => self::FHTranslate("The server did not set a valid filename."), "errorcode" => "invalid_filename");
					else if (isset($options["limit"]) && $options["limit"] > -1 && filesize($files[0]["file"]) > $options["limit"])  $result = array("success" => false, "error" => self::FHTranslate("The server file size limit was exceeded."), "errorcode" => "file_too_large");
					else
					{
						@copy($files[0]["file"], $filename);

						$result = array(
							"success" => true
						);
					}
				}
			}

			if ($result["success"] && isset($options["result_callback"]) && is_callable($options["result_callback"]))  call_user_func_array($options["result_callback"], array(&$result, $filename, $name, strtolower($files[0]["ext"]), $files[0], (isset($options["result_callback_opts"]) ? $options["result_callback_opts"] : false)));

			if (isset($options["return_result"]) && $options["return_result"])  return $result;

			header("Content-Type: application/json");

			echo json_encode($result, JSON_UNESCAPED_SLASHES);

			exit();
		}

		public static function FHTranslate()
		{
			$args = func_get_args();
			if (!count($args))  return "";

			return call_user_func_array((defined("CS_TRANSLATE_FUNC") && function_exists(CS_TRANSLATE_FUNC) ? CS_TRANSLATE_FUNC : "sprintf"), $args);
		}
	}
?>