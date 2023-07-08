<?php
	// File Explorer File System Helper class.
	// (C) 2020 CubicleSoft.  All Rights Reserved.

	class FileExplorerFSHelper
	{
		protected static $usercache = array(), $groupcache = array();

		public static function GetRequestVar($name)
		{
			if (isset($_POST[$name]))  return $_POST[$name];
			else if (isset($_GET[$name]))  return $_GET[$name];
			else  return false;
		}

		public static function GetSanitizedPath($basedir, $name, $allowdotfolders = false, $extrapath = "")
		{
			$path = self::GetRequestVar($name);
			if ($path === false)  return false;

			$path = @json_decode($path, true);
			if (!is_array($path))  return false;

			$result = array();

			foreach ($path as $id)
			{
				if (!is_string($id) || $id === "." || $id === "..")  return false;

				if ($id === "")  continue;

				if ($id[0] === "." && !$allowdotfolders)  return false;

				$result[] = $id;
			}

			$result = @realpath(rtrim($basedir, "/") . "/" . implode("/", $result));
			if ($result === false)  return false;

			$result = str_replace("\\", "/", $result);

			if ($extrapath !== "")  $result .= "/" . $extrapath;

			return $result;
		}

		public static function CleanFilename($file)
		{
			$file = str_replace(array("/", "\\", "<", ">", ":", "?", "*", "|"), "", $file);

			return ($file !== "" && $file !== "." && $file !== ".." ? $file : false);
		}

		public static function GetSanitizedFile($name)
		{
			$file = self::GetRequestVar($name);
			if ($file === false)  return false;

			return self::CleanFilename($file);
		}

		public static function GetSanitizedFileAndExtraPath(&$extrapath, $name, $allowdotfolders = false)
		{
			$extrapath = "";

			$file = self::GetRequestVar($name);
			if ($file === false)  return false;

			$file = str_replace("\\", "/", str_replace(array("<", ">", ":", "?", "*", "|"), "", $file));
			$pos = strrpos($file, "/");
			if ($pos !== false)
			{
				$path = explode("/", substr($file, 0, $pos));
				$file = substr($file, $pos + 1);

				$extrapath = array();
				foreach ($path as $pathseg)
				{
					if ($pathseg !== "" && $pathseg !== "." && $pathseg !== "..")
					{
						if ($pathseg[0] === "." && !$allowdotfolders)  return false;

						$extrapath[] = $pathseg;
					}
				}

				$extrapath = implode("/", $extrapath);
			}

			if ($file === "" || $file === "." || $file === "..")  return false;

			return $file;
		}

		public static function GetFileExt($file, $default = false)
		{
			$pos = strrpos($file, ".");
			if ($pos === false)  return $default;

			return strtolower(substr($file, $pos + 1));
		}

		public static function ExtractAllowedExtensions($exts)
		{
			$result = array();
			$exts2 = explode(",", $exts);
			foreach ($exts2 as $ext)
			{
				$ext = trim($ext);
				$ext = trim($ext, ".");

				if ($ext !== "")  $result[strtolower($ext)] = true;
			}

			return $result;
		}

		public static function HasAllowedExt(&$allowedexts, $allowempty, $file)
		{
			if ($allowedexts === false)  return false;
			if ($allowedexts === true)  return true;

			$pos = strrpos($file, ".");
			if ($pos === false)
			{
				if (!$allowempty)  return false;
			}
			else
			{
				$ext = strtolower(substr($file, $pos + 1));
				if (!isset($allowedexts[$ext]))  return false;
			}

			return true;
		}

		public static function GetPathDepth($path, $basedir)
		{
			return 5;
		}

		public static function GetEntryHash($type, $file, &$info)
		{
			return md5($type . "|" . $file . "|" . $info["mode"] . "|" . $info["uid"] . "|" . $info["gid"] . "|" . $info["size"] . "|" . $info["mtime"]);
		}

		public static function IsRecycleBin($path, &$options)
		{
			if (!isset($options["recycle_to"]) || !is_string($options["recycle_to"]))  return false;

			$recyclepath = $options["base_dir"] . "/" . $options["recycle_to"] . "/";

			return !strncmp($path . "/", $recyclepath, strlen($recyclepath));
		}

		public static function ConvertBytesToUserStr($num)
		{
			$num = (double)$num;

			if ($num < 0)  return "0 " . self::FETranslate("bytes");
			if ($num < 1024)  return number_format($num, 0) . " " . self::FETranslate("bytes");
			if ($num < 1048576)  return str_replace(".0 ", "", number_format($num / 1024, 1)) . " KB";
			if ($num < 1073741824)  return str_replace(".0 ", "", number_format($num / 1048576, 1)) . " MB";
			if ($num < 1099511627776.0)  return str_replace(".0 ", "", number_format($num / 1073741824.0, 1)) . " GB";
			if ($num < 1125899906842624.0)  return str_replace(".0 ", "", number_format($num / 1099511627776.0, 1)) . " TB";

			return str_replace(".0 ", "", number_format($num / 1125899906842624.0, 1)) . " PB";
		}

		public static function GetUserInfoByID($uid)
		{
			if (!function_exists("posix_getpwuid"))  return false;

			if (!isset(self::$usercache[$uid]))
			{
				$user = @posix_getpwuid($uid);
				if ($user === false || !is_array($user))  self::$usercache[$uid] = false;
				else
				{
					self::$usercache[$uid] = $user;
					self::$usercache["_" . $user["name"]] = $user;
				}
			}

			return self::$usercache[$uid];
		}

		public static function GetUserName($uid)
		{
			$user = self::GetUserInfoByID($uid);

			return ($user !== false ? $user["name"] : "");
		}

		public static function GetGroupInfoByID($gid)
		{
			if (!function_exists("posix_getgrgid"))  return false;

			if (!isset(self::$groupcache[$gid]))
			{
				$group = @posix_getgrgid($gid);
				if ($group === false || !is_array($group))  self::$groupcache[$gid] = "";
				else
				{
					self::$groupcache[$gid] = $group;
					self::$groupcache["_" . $group["name"]] = $group;
				}
			}

			return self::$groupcache[$gid];
		}

		public static function GetGroupName($gid)
		{
			$group = self::GetGroupInfoByID($gid);

			return ($group !== false ? $group["name"] : "");
		}

		// Swiped from Barebones CMS SDK.
		public static function GetDestCropAndSize(&$cropx, &$cropy, &$cropw, &$croph, &$destwidth, &$destheight, $srcwidth, $srcheight, $crop, $maxwidth, $maxheight)
		{
			$cropx = 0;
			$cropy = 0;
			$cropw = (int)$srcwidth;
			$croph = (int)$srcheight;

			if ($crop !== "")
			{
				$crop = explode(",", preg_replace('/[^0-9.,]/', "", $crop));
				if (count($crop) == 4 && $crop[0] !== $crop[2] && $crop[1] !== $crop[3] && $crop[0] >= 0 && $crop[1] >= 0 && $crop[2] >= 0 && $crop[3] >= 0 && $crop[0] < $srcwidth && $crop[1] < $srcheight && $crop[2] < $srcwidth && $crop[3] < $srcheight)
				{
					$cropx = (double)$crop[0];
					$cropy = (double)$crop[1];
					$cropw = (double)$crop[2];
					$croph = (double)$crop[3];

					// Normalize.
					if ($cropx > $cropw)
					{
						$temp = $cropx;
						$cropx = $cropw;
						$cropw = $temp;
					}
					if ($cropy > $croph)
					{
						$temp = $cropy;
						$cropy = $croph;
						$croph = $temp;
					}
					if ($cropw < 1.00001 && $croph < 1.00001)
					{
						// Assume percentage of the image.
						$cropx = $cropx * $srcwidth;
						$cropy = $cropy * $srcheight;
						$cropw = $cropw * $srcwidth;
						$croph = $croph * $srcheight;
					}

					$cropw = (int)($cropw - $cropx);
					$croph = (int)($croph - $cropy);
					$cropx = (int)$cropx;
					$cropy = (int)$cropy;
				}
			}

			// Calculate final image width and height.
			if ($cropw <= $maxwidth)
			{
				$destwidth = $cropw;
				$destheight = $croph;
			}
			else
			{
				$destwidth = $maxwidth;
				$destheight = (int)($croph * $destwidth / $cropw);
			}

			if ($destheight > $maxheight)
			{
				$destwidth = (int)($destwidth * $maxheight / $destheight);
				$destheight = $maxheight;
			}
		}

		public static function CropAndScaleImage($data, $crop = "", $maxwidth = false, $maxheight = false)
		{
			@ini_set("memory_limit", "512M");

			// Detect which image library is available to crop and scale the image.
			if (extension_loaded("imagick"))
			{
				// ImageMagick.
				try
				{
					$img = new Imagick();
					$img->readImageBlob($data);
					$info = $img->getImageGeometry();
					$srcwidth = $info["width"];
					$srcheight = $info["height"];

					if ($maxwidth === false)  $maxwidth = $srcwidth;
					if ($maxheight === false)  $maxheight = $srcheight;

					if ($srcwidth <= $maxwidth && $crop === "")  return array("success" => true, "data" => $data);

					// Calculate various points.
					self::GetDestCropAndSize($cropx, $cropy, $cropw, $croph, $destwidth, $destheight, $srcwidth, $srcheight, $crop, $maxwidth, $maxheight);
				}
				catch (Exception $e)
				{
					return array("success" => false, "error" => self::FETranslate("Unable to load image."), "errorcode" => "image_load_failed");
				}

				try
				{
					// Crop the image.
					if ($crop !== "")
					{
						$img->cropImage($cropw, $croph, $cropx, $cropy);

						// Strip out EXIF and 8BIM profiles (if any) since embedded thumbnails no longer match the actual image.
						$profiles = $img->getImageProfiles("*", false);
						foreach ($profiles as $profile)
						{
							if ($profile === "exif" || $profile === "8bim")  $img->removeImageProfile($profile);
						}
					}

					// Resize the image.
					$img->resizeImage($destwidth, $destheight, imagick::FILTER_CATROM, 1);

					// Gather the result.
					return array("success" => true, "data" => $img->getImageBlob());
				}
				catch (Exception $e)
				{
					return array("success" => false, "error" => self::FETranslate("Unable to crop/resize image."), "errorcode" => "image_crop_resize_failed");
				}
			}
			else if (extension_loaded("gd") && function_exists("gd_info"))
			{
				// GD.
				$info = @getimagesizefromstring($data);
				if ($info === false)  return array("success" => false, "error" => self::FETranslate("Unable to load image."), "errorcode" => "image_load_failed");
				$srcwidth = $info[0];
				$srcheight = $info[1];
				$type = $info[2];

				if ($type !== IMAGETYPE_JPEG && $type !== IMAGETYPE_PNG && $type !== IMAGETYPE_GIF)  return array("success" => false, "error" => self::FETranslate("Unsupported image format."), "errorcode" => "unsupported_image_format");

				if ($maxwidth === false)  $maxwidth = $srcwidth;
				if ($maxheight === false)  $maxheight = $srcheight;

				if ($srcwidth <= $maxwidth && $crop === "")  return array("success" => true, "data" => $data);

				// Calculate various points.
				self::GetDestCropAndSize($cropx, $cropy, $cropw, $croph, $destwidth, $destheight, $srcwidth, $srcheight, $crop, $maxwidth, $maxheight);

				$img = @imagecreatefromstring($data);
				if ($img === false)  return array("success" => false, "error" => self::FETranslate("Unable to load image."), "errorcode" => "image_load_failed");
				$data = "";

				$img2 = @imagecreatetruecolor($destwidth, $destheight);
				if ($img2 === false)
				{
					imagedestroy($img);

					return array("success" => false, "error" => self::FETranslate("Unable to crop/resize image."), "errorcode" => "image_crop_resize_failed");
				}

				// Make fully transparent (if relevant).
				if ($type === IMAGETYPE_PNG || $type === IMAGETYPE_GIF)
				{
					$transparent = imagecolorallocatealpha($img2, 0, 0, 0, 127);
					imagecolortransparent($img2, $transparent);
					imagealphablending($img2, false);
					imagesavealpha($img2, true);
					imagefill($img2, 0, 0, $transparent);
				}

				// Copy the source onto the destination, resizing in the process.
				imagecopyresampled($img2, $img, 0, 0, $cropx, $cropy, $destwidth, $destheight, $cropw, $croph);
				imagedestroy($img);

				ob_start();
				if ($type === IMAGETYPE_JPEG)  @imagejpeg($img2, NULL, 85);
				else if ($type === IMAGETYPE_PNG)  @imagepng($img2);
				else if ($type === IMAGETYPE_GIF)  @imagegif($img2);
				$data = ob_get_contents();
				ob_end_clean();

				imagedestroy($img2);

				return array("success" => true, "data" => $data);
			}

			return array("success" => false, "error" => self::FETranslate("A supported image library is not installed/configured."), "errorcode" => "missing_image_library");
		}

		public static function GetTooltip($path, $file, $windows, $type, &$info)
		{
			$tooltip = array();
			if (strlen($file) > 35)  $tooltip[] = $file;

			if (!$windows)
			{
				$type2 = $info["mode"] & 0170000;

				if ($type2 === 0100000)  $mode = "-";
				else if ($type2 === 0040000)  $mode = "d";
				else if ($type2 === 0140000)  $mode = "s";
				else if ($type2 === 0120000)  $mode = "l";
				else if ($type2 === 0060000)  $mode = "b";
				else if ($type2 === 0020000)  $mode = "c";
				else if ($type2 === 0010000)  $mode = "p";
				else  $mode = "u";

				$mode .= ($info["mode"] & 0x0100 ? "r" : "-");
				$mode .= ($info["mode"] & 0x0080 ? "w" : "-");
				$mode .= ($info["mode"] & 0x0040 ? ($info["mode"] & 0x0800 ? "s" : "x") : ($info["mode"] & 0x0800 ? "S" : "-"));

				$mode .= ($info["mode"] & 0x0020 ? "r" : "-");
				$mode .= ($info["mode"] & 0x0010 ? "w" : "-");
				$mode .= ($info["mode"] & 0x0008 ? ($info["mode"] & 0x0400 ? "s" : "x") : ($info["mode"] & 0x0400 ? "S" : "-"));

				$mode .= ($info["mode"] & 0x0004 ? "r" : "-");
				$mode .= ($info["mode"] & 0x0002 ? "w" : "-");
				$mode .= ($info["mode"] & 0x0001 ? ($info["mode"] & 0x0200 ? "t" : "x") : ($info["mode"] & 0x0200 ? "T" : "-"));

				$tooltip[] = self::FETranslate("Mode: %s", $mode);

				$username = self::GetUserName($info["uid"]);
				$groupname = self::GetGroupName($info["gid"]);

				if ($username === false)  $tooltip[] = self::FETranslate("Owner: %u", $info["uid"]);
				else  $tooltip[] = self::FETranslate("Owner: %s (%u)", $username, $info["uid"]);

				if ($groupname === false)  $tooltip[] = self::FETranslate("Group: %u", $info["gid"]);
				else  $tooltip[] = self::FETranslate("Group: %s (%u)", $groupname, $info["gid"]);
			}

			if ($type === "file")  $tooltip[] = self::FETranslate("Size: %s", self::ConvertBytesToUserStr($info["size"]));

			$tooltip[] = self::FETranslate("Modified: %s", date(self::FETranslate("n/j/Y g:i A"), $info["mtime"]));

			return implode("\n", $tooltip);
		}

		public static function BuildEntry($path, $file, $type, $depth, &$options)
		{
			$info = @stat($path . "/" . $file);
			if ($info === false)  return false;

			$entry = array(
				"id" => $file,
				"name" => $file,
				"type" => $type,
				"hash" => self::GetEntryHash($type, $file, $info),
				"tooltip" => self::GetTooltip($path, $file, $options["windows"], $type, $info)
			);

			if ($options["protect_depth"] > $depth + 1)  $entry["attrs"] = array("canmodify" => false);

			if ($type === "file")
			{
				$entry["size"] = $info["size"];

				if (isset($options["thumbs_dir"]))
				{
					$ext = self::GetFileExt($file);

					if ($ext === "jpg" || $ext === "jpeg" || $ext === "png" || $ext === "gif")
					{
						if (isset($options["base_url"]) && $info["size"] < 25000)  $entry["thumb"] = $options["base_url"] . substr($path, strlen($options["base_dir"])) . "/" . $file;
						else if ($info["size"] < 10000000)
						{
							@mkdir($options["thumbs_dir"] . "/" . substr($entry["hash"], 0, 3), 0775);

							$filename = "/" . substr($entry["hash"], 0, 3) . "/" . $entry["hash"] . "." . $ext;

							// Generate thumbnail if less than 5 seconds have passed.
							if (!file_exists($options["thumbs_dir"] . $filename) && $options["started"] >= time() - 5)
							{
								$result = self::CropAndScaleImage(file_get_contents($path . "/" . $file), "", 200, 200);
								if ($result["success"])  file_put_contents($options["thumbs_dir"] . $filename, $result["data"]);
							}

							if (file_exists($options["thumbs_dir"] . $filename))  $entry["thumb"] = $options["thumbs_url"] . $filename;
							else if (isset($options["thumb_create_url"]) && $options["started"] >= time() - 5)  $entry["thumb"] = $options["thumb_create_url"] . (strpos($options["thumb_create_url"], "?") !== false ? "&" : "?") . "path=" . urlencode(json_encode(explode("/", substr($path, strlen($options["base_dir"]))), JSON_UNESCAPED_SLASHES)) . "&id=" . urlencode($file);
						}
					}
					else if ($ext === "svg" && $info["size"] < 100000)
					{
						if (isset($options["base_url"]))  $entry["thumb"] = $options["base_url"] . substr($path, strlen($options["base_dir"])) . "/" . $file;
						else
						{
							@mkdir($options["thumbs_dir"] . "/" . substr($entry["hash"], 0, 3), 0775);

							$filename = "/" . substr($entry["hash"], 0, 3) . "/" . $entry["hash"] . "." . $ext;

							if (!file_exists($options["thumbs_dir"] . $filename))  @copy($options["thumbs_dir"] . $filename, $path . "/" . $file);

							$entry["thumb"] = $options["thumbs_url"] . $filename;
						}
					}
				}
			}

			return $entry;
		}

		// Refresh folder.
		protected static function ProcessRefreshAction(&$options)
		{
			$path = self::GetSanitizedPath($options["base_dir"], "path", $options["dot_folders"]);

			if (!isset($options["refresh"]) || !$options["refresh"])  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "refresh_not_allowed");
			else if ($path === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid path specified."), "errorcode" => "invalid_path");
			else
			{
				$dir = @opendir($path);

				if (!$dir)  $result = array("success" => false, "error" => self::FETranslate("The server was unable to open the path."), "errorcode" => "path_open_failed");
				else
				{
					if (is_bool($options["allowed_exts"]))  $allowedexts = $options["allowed_exts"];
					else  $allowedexts = self::ExtractAllowedExtensions($options["allowed_exts"]);

					$depth = self::GetPathDepth($path, $options["base_dir"]);

					@set_time_limit(0);

					$result = array(
						"success" => true,
						"entries" => array()
					);

					while (($file = readdir($dir)) !== false)
					{
						if ($file === "." || $file === "..")  continue;

						if (is_dir($path . "/" . $file))
						{
							if ($file[0] !== "." || $options["dot_folders"])
							{
								$entry = self::BuildEntry($path, $file, "folder", $depth, $options);
								if ($entry !== false)  $result["entries"][] = $entry;
							}
						}
						else if (self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $file))
						{
							$entry = self::BuildEntry($path, $file, "file", $depth, $options);
							if ($entry !== false)  $result["entries"][] = $entry;
						}
					}

					closedir($dir);
				}
			}

			return $result;
		}

		// Thumbnails.
		protected static function ProcessThumnailAction(&$options)
		{
			$path = self::GetSanitizedPath($options["base_dir"], "path", $options["dot_folders"]);
			$file = self::GetSanitizedFile("id");

			if (!isset($options["thumb_create_url"]) || !is_string($options["thumb_create_url"]))  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "thumbnail_not_allowed");
			else if ($path === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid path specified."), "errorcode" => "invalid_path");
			else if ($file === false)  $result = array("success" => false, "error" => self::FETranslate("Missing file ID.  Expected string."), "errorcode" => "missing_id");
			else if (!file_exists($path . "/" . $file) || is_dir($path . "/" . $file))  $result = array("success" => false, "error" => self::FETranslate("File does not exist or is a directory."), "errorcode" => "invalid_file");
			else
			{
				$ext = self::GetFileExt($file);
				if ($ext === false)  $result = array("success" => false, "error" => self::FETranslate("File is missing a file extension."), "errorcode" => "no_file_ext");
				else if ($ext !== "jpg" && $ext !== "jpeg" && $ext !== "png" && $ext !== "gif")  $result = array("success" => false, "error" => self::FETranslate("Thumbnails can only be made of JPG, PNG, and GIF images."), "errorcode" => "invalid_ext");
				else
				{
					$info = @stat($path . "/" . $file);

					$hash = self::GetEntryHash("file", $file, $info);

					@mkdir($options["thumbs_dir"] . "/" . substr($hash, 0, 3), 0775);

					$filename = "/" . substr($hash, 0, 3) . "/" . $hash . "." . $ext;

					// Generate thumbnail.
					if (!file_exists($options["thumbs_dir"] . $filename) && $info["size"] < 10000000)
					{
						$result = self::CropAndScaleImage(file_get_contents($path . "/" . $file), "", 200, 200);
						if ($result["success"])  file_put_contents($options["thumbs_dir"] . $filename, $result["data"]);
					}

					if (!file_exists($options["thumbs_dir"] . $filename))  $result = array("success" => false, "error" => self::FETranslate("Failed to create the thumbnail image.  Image is invalid, is too large, or an image processing library is not available."), "errorcode" => "internal_error");
					else
					{
						header("Location: " . $options["thumbs_url"] . $filename);

						exit();
					}
				}
			}

			return $result;
		}

		// Rename.
		protected static function ProcessRenameAction(&$options)
		{
			$path = self::GetSanitizedPath($options["base_dir"], "path", $options["dot_folders"]);
			$file = self::GetSanitizedFile("id");
			$newname = self::GetSanitizedFile("newname");

			if (!isset($options["rename"]) || !$options["rename"])  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "rename_not_allowed");
			else if ($path === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid path specified."), "errorcode" => "invalid_path");
			else if ($file === false)  $result = array("success" => false, "error" => self::FETranslate("Missing file ID.  Expected string."), "errorcode" => "missing_id");
			else if (!file_exists($path . "/" . $file))  $result = array("success" => false, "error" => self::FETranslate("Item to rename does not exist."), "errorcode" => "item_missing");
			else if ($newname === false)  $result = array("success" => false, "error" => self::FETranslate("Missing new name.  Expected string."), "errorcode" => "missing_newname");
			else if (self::IsRecycleBin($path, $options))  $result = array("success" => false, "error" => self::FETranslate("Items in the recycling bin cannot be renamed."), "errorcode" => "access_denied");
			else
			{
				$depth = self::GetPathDepth($path, $options["base_dir"]);

				if ($depth < $options["protect_depth"])  $result = array("success" => false, "error" => self::FETranslate("This folder cannot be modified."), "errorcode" => "access_denied");
				else if (is_dir($path . "/" . $file))
				{
					if ($file[0] === "." && !$options["dot_folders"])  $result = array("success" => false, "error" => self::FETranslate("The directory cannot be modified."), "errorcode" => "access_denied");
					else if ($newname[0] === "." && !$options["dot_folders"])  $result = array("success" => false, "error" => self::FETranslate("The new directory name is not allowed."), "errorcode" => "invalid_newname");
					else  $result = false;
				}
				else
				{
					if (is_bool($options["allowed_exts"]))  $allowedexts = $options["allowed_exts"];
					else  $allowedexts = self::ExtractAllowedExtensions($options["allowed_exts"]);

					if (!self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $file))  $result = array("success" => false, "error" => self::FETranslate("Original file extension is not allowed."), "errorcode" => "access_denied");
					else if (!self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $newname))  $result = array("success" => false, "error" => self::FETranslate("New file extension is not allowed."), "errorcode" => "access_denied");
					else  $result = false;
				}

				if ($result === false)
				{
					if (@rename($path . "/" . $file, $path . "/" . $newname) === false)  $result = array("success" => false, "error" => self::FETranslate("Rename operation failed."), "errorcode" => "rename_failed");
					else if (($entry = self::BuildEntry($path, $newname, (is_dir($path . "/" . $newname) ? "folder" : "file"), $depth, $options)) === false)  $result = array("success" => false, "error" => self::FETranslate("Unable to build the response entry."), "errorcode" => "build_entry_failed");
					else
					{
						$result = array(
							"success" => true,
							"entry" => $entry
						);
					}
				}
			}

			return $result;
		}

		public static function IsValidUTF8($data)
		{
			$x = 0;
			$y = strlen($data);
			while ($x < $y)
			{
				$tempchr = ord($data[$x]);
				if (($tempchr >= 0x20 && $tempchr <= 0x7E) || $tempchr == 0x09 || $tempchr == 0x0A || $tempchr == 0x0D)  $x++;
				else if ($tempchr < 0xC2)  return false;
				else
				{
					$left = $y - $x;
					if ($left > 1)  $tempchr2 = ord($data[$x + 1]);
					else  return false;

					if (($tempchr >= 0xC2 && $tempchr <= 0xDF) && ($tempchr2 >= 0x80 && $tempchr2 <= 0xBF))  $x += 2;
					else
					{
						if ($left > 2)  $tempchr3 = ord($data[$x + 2]);
						else  return false;

						if ($tempchr3 < 0x80 || $tempchr3 > 0xBF)  return false;

						if ($tempchr == 0xE0 && ($tempchr2 >= 0xA0 && $tempchr2 <= 0xBF))  $x += 3;
						else if ((($tempchr >= 0xE1 && $tempchr <= 0xEC) || $tempchr == 0xEE || $tempchr == 0xEF) && ($tempchr2 >= 0x80 && $tempchr2 <= 0xBF))  $x += 3;
						else if ($tempchr == 0xED && ($tempchr2 >= 0x80 && $tempchr2 <= 0x9F))  $x += 3;
						else
						{
							if ($left > 3)  $tempchr4 = ord($data[$x + 3]);
							else  return false;

							if ($tempchr4 < 0x80 || $tempchr4 > 0xBF)  return false;

							if ($tempchr == 0xF0 && ($tempchr2 >= 0x90 && $tempchr2 <= 0xBF))  $x += 4;
							else if (($tempchr >= 0xF1 && $tempchr <= 0xF3) && ($tempchr2 >= 0x80 && $tempchr2 <= 0xBF))  $x += 4;
							else if ($tempchr == 0xF4 && ($tempchr2 >= 0x80 && $tempchr2 <= 0x8F))  $x += 4;
							else  return false;
						}
					}
				}
			}

			return true;
		}

		// File Info.
		protected static function ProcessFileInfoAction(&$options)
		{
			$path = self::GetSanitizedPath($options["base_dir"], "path", $options["dot_folders"]);

			$name = self::GetRequestVar("id");
			if ($name !== false)  $name = self::CleanFilename($name);

			if (!isset($options["file_info"]) || !$options["file_info"])  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "file_info_not_allowed");
			else if ($path === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid path specified."), "errorcode" => "invalid_path");
			else if ($name === false || $name === "")  $result = array("success" => false, "error" => self::FETranslate("Invalid file ID specified."), "errorcode" => "invalid_id");
			else if (!file_exists($path . "/" . $name) || !is_file($path . "/" . $name))  $result = array("success" => false, "error" => self::FETranslate("The specified file does not exist or is not a file."), "errorcode" => "invalid_file");
			else
			{
				// Check allowed file extensions.
				if (is_bool($options["allowed_exts"]))  $allowedexts = $options["allowed_exts"];
				else  $allowedexts = self::ExtractAllowedExtensions($options["allowed_exts"]);

				$info = @stat($path . "/" . $name);
				$fp = @fopen($path . "/" . $name, "rb");

				if (!self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $name))  $result = array("success" => false, "error" => self::FETranslate("The file extension is not allowed."), "errorcode" => "invalid_file_ext");
				else if ($info === false)  $result = array("success" => false, "error" => self::FETranslate("Unable to retrieve information about the file."), "errorcode" => "stat_failed");
				else if ($fp === false)  $result = array("success" => false, "error" => self::FETranslate("Unable to open the file."), "errorcode" => "open_failed");
				else
				{
					$data = @fread($fp, 65536);

					fclose($fp);

					$ext = self::GetFileExt($name, "");
					$text = self::IsValidUTF8($data);
					$browser = false;

					$pos = strrpos($data, "\n");
					$pos2 = strrpos($data, "\r\n");
					$pos3 = strrpos($data, "\r");

					if ($pos2 !== false)
					{
						$textend = "\r\n";
						$data = substr($data, 0, $pos2);
					}
					else if ($pos !== false)
					{
						$textend = "\n";
						$data = substr($data, 0, $pos);
					}
					else if ($pos3 !== false)
					{
						$textend = "\r";
						$data = substr($data, 0, $pos3);
					}
					else
					{
						$textend = "\n";
					}

					if (substr($data, 0, 6) === "GIF87a" || substr($data, 0, 6) === "GIF89a")  { $mimetype = "image/gif";  $browser = true; }
					else if (substr($data, 0, 8) === "\x89PNG\x0D\x0A\x1A\x0A")  { $mimetype = "image/png";  $browser = true; }
					else if (substr($data, 0, 2) === "\xFF\xD8" || (!$text && ($ext === "jpg" || $ext === "jpeg")))  { $mimetype = "image/jpeg";  $browser = true; }
					else if ($text && $ext === "svg")  { $mimetype = "image/svg";  $browser = true; }
					else if (substr($data, 0, 3) === "ID3" || (substr($data, 0, 1) === "\xFF" && ord(substr($data, 1, 1)) >= 0xE0) || (!$text && $ext === "mp3"))  { $mimetype = "audio/mp3";  $browser = true; }
					else if (substr($data, 4, 8) === "ftypmp42" || substr($data, 4, 8) === "ftypMSNV" || substr($data, 4, 8) === "ftypisom" || (!$text && $ext === "mp4"))  { $mimetype = "video/mp4";  $browser = true; }
					else if ($text && (stripos($data, "<!DOCTYPE") !== false || stripos($data, "<html") !== false || $ext === "html" || $ext === "htm"))  { $mimetype = "text/html";  $browser = true; }
					else if ($text && ($ext === "xml" || stripos($data, "<" . "?xml ") !== false))  $mimetype = "text/xml";
					else if ($text && $ext === "css")  $mimetype = "text/css";
					else if ($text && $ext === "diff")  $mimetype = "text/diff";
					else if ($text && $ext === "js")  $mimetype = "text/javascript";
					else if ($text && $ext === "json")  $mimetype = "application/json";
					else if ($text && $ext === "md")  $mimetype = "text/markdown";
					else if ($text && $ext === "php")  $mimetype = "application/php";
					else if ($text)  $mimetype = "text/plain";
					else  $mimetype = "application/octet-stream";

					$result = array(
						"success" => true,
						"windows" => $options["windows"],
						"url" => (isset($options["base_url"]) ? $options["base_url"] . substr($path, strlen($options["base_dir"])) . "/" . $name : false),
						"path" => self::GetRequestVar("path"),
						"id" => self::GetRequestVar("id"),
						"recycle_bin" => self::IsRecycleBin($path, $options),
						"name" => $name,
						"file_key" => substr($path, strlen($options["base_dir"])) . "/" . $name,
						"ext" => $ext,
						"mime_type" => $mimetype,
						"browser" => $browser,
						"text" => $text,
						"text_end" => $textend,
						"stat" => $info
					);
				}
			}

			return $result;
		}

		// Load File.
		protected static function ProcessLoadFileAction(&$options)
		{
			$path = self::GetSanitizedPath($options["base_dir"], "path", $options["dot_folders"]);

			$name = self::GetRequestVar("id");
			if ($name !== false)  $name = self::CleanFilename($name);

			if (!isset($options["load_file"]) || !$options["load_file"])  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "load_file_not_allowed");
			else if ($path === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid path specified."), "errorcode" => "invalid_path");
			else if ($name === false || $name === "")  $result = array("success" => false, "error" => self::FETranslate("Invalid file ID specified."), "errorcode" => "invalid_id");
			else if (!file_exists($path . "/" . $name) || !is_file($path . "/" . $name))  $result = array("success" => false, "error" => self::FETranslate("The specified file does not exist or is not a file."), "errorcode" => "invalid_file");
			else
			{
				// Check allowed file extensions.
				if (is_bool($options["allowed_exts"]))  $allowedexts = $options["allowed_exts"];
				else  $allowedexts = self::ExtractAllowedExtensions($options["allowed_exts"]);

				$info = @stat($path . "/" . $name);
				$data = @file_get_contents($path . "/" . $name);

				if (!self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $name))  $result = array("success" => false, "error" => self::FETranslate("The file extension is not allowed."), "errorcode" => "invalid_file_ext");
				else if ($info === false)  $result = array("success" => false, "error" => self::FETranslate("Unable to retrieve information about the file."), "errorcode" => "stat_failed");
				else if ($data === false)  $result = array("success" => false, "error" => self::FETranslate("Unable to read the file."), "errorcode" => "read_failed");
				else
				{
					$result = array(
						"success" => true,
						"hash" => md5($data),
						"data" => base64_encode($data),
						"stat" => $info
					);
				}
			}

			return $result;
		}

		// Save File.
		protected static function ProcessSaveFileAction(&$options)
		{
			$path = self::GetSanitizedPath($options["base_dir"], "path", $options["dot_folders"]);

			$name = self::GetRequestVar("id");
			if ($name !== false)  $name = self::CleanFilename($name);

			$userdata = self::GetRequestVar("data");

			if (!isset($options["save_file"]) || !$options["save_file"])  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "save_file_not_allowed");
			else if ($path === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid path specified."), "errorcode" => "invalid_path");
			else if ($name === false || $name === "")  $result = array("success" => false, "error" => self::FETranslate("Invalid file ID specified."), "errorcode" => "invalid_id");
			else if (!file_exists($path . "/" . $name) || !is_file($path . "/" . $name))  $result = array("success" => false, "error" => self::FETranslate("The specified file does not exist or is not a file."), "errorcode" => "invalid_file");
			else if ($userdata === false)  $result = array("success" => false, "error" => self::FETranslate("Missing data."), "errorcode" => "missing_data");
			else
			{
				// Check allowed file extensions.
				if (is_bool($options["allowed_exts"]))  $allowedexts = $options["allowed_exts"];
				else  $allowedexts = self::ExtractAllowedExtensions($options["allowed_exts"]);

				$userhash = self::GetRequestVar("hash");
				$startpos = self::GetRequestVar("start");
				$endpos = self::GetRequestVar("end");
				$userdata = @base64_decode($userdata);

				$data = @file_get_contents($path . "/" . $name);

				if (!self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $name))  $result = array("success" => false, "error" => self::FETranslate("The file extension is not allowed."), "errorcode" => "invalid_file_ext");
				else if ($data === false)  $result = array("success" => false, "error" => self::FETranslate("Unable to read the existing file."), "errorcode" => "read_failed");
				else if ($userdata === false)  $result = array("success" => false, "error" => self::FETranslate("Unable to decode data."), "errorcode" => "data_decode_failed");
				else if ($userhash !== false && $userhash !== md5($data))  $result = array("success" => false, "error" => self::FETranslate("The existing file hash is different."), "errorcode" => "file_changed");
				else if ($userhash !== false && ($startpos === false || (int)$startpos < 0 || (int)$startpos > strlen($data)))  $result = array("success" => false, "error" => self::FETranslate("Missing or invalid start file position."), "errorcode" => "invalid_start");
				else if ($userhash !== false && ($endpos === false || (int)$endpos < 0 || (int)$endpos > strlen($data) || (int)$endpos < $startpos))  $result = array("success" => false, "error" => self::FETranslate("Missing or invalid end file position."), "errorcode" => "invalid_end");
				else
				{
					$data = ($userhash === false ? $userdata : substr($data, 0, $startpos) . $userdata . substr($data, $endpos));

					if (!@file_put_contents($path . "/" . $name, $data))  $result = array("success" => false, "error" => self::FETranslate("Unable to write file."), "errorcode" => "write_file_failed");
					else
					{
						$info = @stat($path . "/" . $name);

						$result = array(
							"success" => true,
							"hash" => md5($data),
							"stat" => $info
						);
					}
				}
			}

			return $result;
		}

		// New Folder.
		protected static function ProcessNewFolderAction(&$options)
		{
			$name = self::GetSanitizedFileAndExtraPath($extrapath, "name", $options["dot_folders"]);
			$path = self::GetSanitizedPath($options["base_dir"], "path", $options["dot_folders"], $extrapath);

			if (!isset($options["new_folder"]) || !$options["new_folder"])  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "new_folder_not_allowed");
			else if ($path === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid path specified."), "errorcode" => "invalid_path");
			else if (self::IsRecycleBin($path, $options))  $result = array("success" => false, "error" => self::FETranslate("Cannot create folders in the recycling bin."), "errorcode" => "access_denied");
			else if ($name !== false && $name[0] === "." && !$options["dot_folders"])  $result = array("success" => false, "error" => self::FETranslate("The new folder name is not allowed."), "errorcode" => "invalid_name");
			else
			{
				$depth = self::GetPathDepth($path, $options["base_dir"]);

				if ($depth < $options["protect_depth"])  $result = array("success" => false, "error" => self::FETranslate("This folder cannot be modified."), "errorcode" => "access_denied");
				else
				{
					if ($name === false)
					{
						$num = 1;
						do
						{
							$name = self::FETranslate("New Folder" . ($num > 1 ? " (%u)" : ""), $num);
							$num++;
						} while (file_exists($path . "/" . $name));
					}

					@mkdir($path . "/" . $name, 0775, true);

					if (!file_exists($path . "/" . $name))  $result = array("success" => false, "error" => self::FETranslate("Unable to create folder."), "errorcode" => "mkdir_failed");
					else if (($entry = self::BuildEntry($path, $name, "folder", $depth, $options)) === false)  $result = array("success" => false, "error" => self::FETranslate("Unable to build the response entry."), "errorcode" => "build_entry_failed");
					else
					{
						$result = array(
							"success" => true,
							"entry" => $entry
						);
					}
				}
			}

			return $result;
		}

		// New File.
		protected static function ProcessNewFileAction(&$options)
		{
			$path = self::GetSanitizedPath($options["base_dir"], "path", $options["dot_folders"]);

			if (!isset($options["new_file"]) || !is_string($options["new_file"]))  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "new_file_not_allowed");
			else if ($path === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid path specified."), "errorcode" => "invalid_path");
			else if (self::IsRecycleBin($path, $options))  $result = array("success" => false, "error" => self::FETranslate("Cannot create files in the recycling bin."), "errorcode" => "access_denied");
			else
			{
				$depth = self::GetPathDepth($path, $options["base_dir"]);

				if ($depth < $options["protect_depth"])  $result = array("success" => false, "error" => self::FETranslate("This folder cannot be modified."), "errorcode" => "access_denied");
				else
				{
					$options["new_file"] = trim($options["new_file"], ".");

					$num = 1;
					do
					{
						$name = self::FETranslate("New File" . ($num > 1 ? " (%1\$u)" : "") . ".%2\$s", $num, $options["new_file"]);
						$num++;
					} while (file_exists($path . "/" . $name));

					@file_put_contents($path . "/" . $name, "");

					if (!file_exists($path . "/" . $name))  $result = array("success" => false, "error" => self::FETranslate("Unable to create file."), "errorcode" => "create_file_failed");
					else if (($entry = self::BuildEntry($path, $name, "file", $depth, $options)) === false)  $result = array("success" => false, "error" => self::FETranslate("Unable to build the response entry."), "errorcode" => "build_entry_failed");
					else
					{
						$result = array(
							"success" => true,
							"entry" => $entry
						);
					}
				}
			}

			return $result;
		}

		// Upload.
		protected static function ProcessUploadAction(&$options)
		{
			$name = self::GetSanitizedFileAndExtraPath($extrapath, "name", $options["dot_folders"]);
			$path = self::GetSanitizedPath($options["base_dir"], "path", $options["dot_folders"], $extrapath);
			$size = self::GetRequestVar("size");
			$queuestarted = self::GetRequestVar("queuestarted");
			$currpath = self::GetSanitizedPath($options["base_dir"], "currpath", $options["dot_folders"]);

			if (!isset($options["upload"]) || !$options["upload"])  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "upload_not_allowed");
			else if ($path === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid path specified."), "errorcode" => "invalid_path");
			else if (self::IsRecycleBin($path, $options))  $result = array("success" => false, "error" => self::FETranslate("Cannot upload to the recycling bin."), "errorcode" => "access_denied");
			else if ($name === false)  $result = array("success" => false, "error" => self::FETranslate("The upload file name is not allowed."), "errorcode" => "invalid_name");
			else if ($size === false || (int)$size < 0)  $result = array("success" => false, "error" => self::FETranslate("The upload file size was not specified or was invalid."), "errorcode" => "invalid_size");
			else if (isset($options["upload_limit"]) && $options["upload_limit"] > -1 && (int)$size > $options["upload_limit"])  $result = array("success" => false, "error" => self::FETranslate("The file to be uploaded is too large.  Server limit is %u.", self::ConvertBytesToUserStr($options["upload_limit"])), "errorcode" => "invalid_size");
			else if ($queuestarted === false || (int)$queuestarted < 0)  $result = array("success" => false, "error" => self::FETranslate("The upload queue start time was not specified or was invalid."), "errorcode" => "invalid_queuestarted");
			else
			{
				$depth = self::GetPathDepth($path, $options["base_dir"]);

				// Check allowed file extensions.
				if (is_bool($options["allowed_exts"]))  $allowedexts = $options["allowed_exts"];
				else  $allowedexts = self::ExtractAllowedExtensions($options["allowed_exts"]);

				if ($depth < $options["protect_depth"])  $result = array("success" => false, "error" => self::FETranslate("This folder cannot be modified."), "errorcode" => "access_denied");
				else if (!self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $name))  $result = array("success" => false, "error" => self::FETranslate("The file extension is not allowed."), "errorcode" => "invalid_file_ext");
				else if ($options["action"] === $options["requestprefix"] . "upload_init")
				{
					$createddir = (!is_dir($path));
					@mkdir($path, 0775, true);

					if (!is_dir($path))  $result = array("success" => false, "error" => self::FETranslate("Unable to create parent folder(s)."), "errorcode" => "mkdir_failed");
					else if (file_exists($path . "/" . $name) && !is_file($path . "/" . $name))  $result = array("success" => false, "error" => self::FETranslate("A non-file item already exists at the upload location."), "errorcode" => "non_file_exists");
					else
					{
						// Remove a previously failed upload.
						@unlink($path . "/" . $name . ".tmp");

						$result = array(
							"success" => true,
						);

						if ($createddir && $currpath !== false && strlen($path) > strlen($currpath) && strncmp($path . "/", $currpath . "/", strlen($currpath) + 1) == 0)
						{
							$pos = strpos($path, "/", strlen($currpath) + 1);
							$file = ($pos !== false ? substr($path, strlen($currpath) + 1, $pos - strlen($currpath) - 1) : substr($path, strlen($currpath) + 1));

							$entry = self::BuildEntry($currpath, $file, "folder", self::GetPathDepth($currpath, $options["base_dir"]), $options);
							if ($entry !== false)  $result["entry"] = $entry;
						}
					}
				}
				else if (!is_dir($path))  $result = array("success" => false, "error" => self::FETranslate("Parent folder(s) do not exist."), "errorcode" => "path_missing");
				else if (file_exists($path . "/" . $name) && !is_file($path . "/" . $name))  $result = array("success" => false, "error" => self::FETranslate("A non-file item already exists at the upload location."), "errorcode" => "non_file_exists");
				else
				{
					if (!class_exists("FileUploadHelper", false))  require_once str_replace("\\", "/", dirname(__FILE__)) . "/file_upload_helper.php";

					$options2 = array(
						"filename" => $path . "/" . $name . ".tmp",
						"fixed_filename" => true,
						"limit" => (int)$size,
						"return_result" => true
					);

					$_REQUEST["fileuploader"] = 1;
					$result = FileUploadHelper::HandleUpload("file", $options2);

					clearstatcache();

					// Finalize the file.
					if ($result["success"] && @filesize($path . "/" . $name . ".tmp") >= $size)
					{
						// Move an existing item to the recycling bin.
						if (file_exists($path . "/" . $name) && isset($options["recycle_to"]) && is_string($options["recycle_to"]))
						{
							$recyclepath = $options["base_dir"] . "/" . $options["recycle_to"] . "/" . date("Y-m-d_H-i-s", $queuestarted) . substr($path, strlen($options["base_dir"]));
							@mkdir($recyclepath, 0775, true);

							@rename($path . "/" . $name, $recyclepath . "/" . $name);
							@unlink($path . "/" . $name);
						}

						if (!@rename($path . "/" . $name . ".tmp", $path . "/" . $name))  $result = array("success" => false, "error" => self::FETranslate("Unable to rename temporary file to final location."), "errorcode" => "rename_failed");
						else if ($path === $currpath)
						{
							$entry = self::BuildEntry($path, $name, "file", $depth, $options);
							if ($entry !== false)  $result["entry"] = $entry;
						}
					}
				}
			}

			return $result;
		}

		// Download.
		protected static function ProcessDownloadAction(&$options)
		{
			$windows = $options["windows"];

			$srcpath = self::GetSanitizedPath($options["base_dir"], "path", $options["dot_folders"]);

			$ids = self::GetRequestVar("ids");
			if ($ids !== false)  $ids = @json_decode($ids, true);

			if (!isset($options["download"]) || !is_string($options["download"]))  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "download_not_allowed");
			else if ($srcpath === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid path specified."), "errorcode" => "invalid_path");
			else if (!is_array($ids))  $result = array("success" => false, "error" => self::FETranslate("Invalid IDs specified."), "errorcode" => "invalid_ids");
			else
			{
				// Check allowed file extensions.
				if (is_bool($options["allowed_exts"]))  $allowedexts = $options["allowed_exts"];
				else  $allowedexts = self::ExtractAllowedExtensions($options["allowed_exts"]);

				$pathstack = array();
				foreach ($ids as $id)
				{
					$id = self::CleanFilename($id);

					if ($id !== false)  $pathstack[] = $id;
				}

				if (!class_exists("ZipStreamWriter", false))  require_once str_replace("\\", "/", dirname(__FILE__)) . "/zip_stream_writer.php";

				if (count($pathstack) === 1 && is_file($srcpath . "/" . $pathstack[0]) && self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $pathstack[0]))
				{
					// Convenient function to trigger a download of the desired filename.
					ZipStreamWriter::StartHTTPResponse($pathstack[0]);

					if (isset($options["download_module"]) && $options["download_module"] === "sendfile")
					{
						header("X-Sendfile: " . (isset($options["download_module_prefix"]) ? $options["download_module_prefix"] : "") . $srcpath . "/" . $pathstack[0]);
					}
					else if (isset($options["download_module"]) && $options["download_module"] === "accel-redirect")
					{
						header("X-Accel-Redirect: " . (isset($options["download_module_prefix"]) ? $options["download_module_prefix"] : "") . $srcpath . "/" . $pathstack[0]);
					}
					else
					{
						// Handle the download internally.
						$size = filesize($srcpath . "/" . $pathstack[0]);

						header("Content-Length: " . $size);

						$fp = @fopen($srcpath . "/" . $pathstack[0], "rb");

						while ($size)
						{
							$data = @fread($fp, ($size > 1048576 ? 1048576 : $size));
							if ($data == "")  break;

							echo $data;
							$size -= strlen($data);
						}

						fclose($fp);
					}
				}
				else
				{
					// Generate a ZIP file on the fly.
					ZipStreamWriter::StartHTTPResponse($options["download"]);

					$zip = new ZipStreamWriter();
					$zip->Init();

					while (count($pathstack))
					{
						$path = array_shift($pathstack);
						$srcpath2 = $srcpath . "/" . $path;

						$info = @stat($srcpath2);
						if ($info === false)  continue;

						if (is_dir($srcpath2))
						{
							$options2 = array(
								"last_modified" => $info["mtime"],
								"extra_fields" => array()
							);

							// NTFS timestamps.
							ZipStreamWriter::AppendNTFSExtraField($options2["extra_fields"], $info["mtime"], $info["atime"], $info["ctime"]);

							if (!$windows)
							{
								// UNIX timestamps + uid/gid.
								ZipStreamWriter::AppendUNIXExtraField($options2["extra_fields"], $info["atime"], $info["mtime"], $info["uid"], $info["gid"]);

								$options2["unix_attrs"] = $info["mode"];
							}

							$zip->AddDirectory($path, $options2);
							if ($zip->BytesAvailable() >= 65536)  echo $zip->Read();

							$dir = @opendir($srcpath2);
							if ($dir)
							{
								while (($file = readdir($dir)) !== false)
								{
									if ($file === "." || $file === "..")  continue;

									$filename = $srcpath2 . "/" . $file;

									if (is_dir($filename))  $pathstack[] = $path . "/" . $file;
									else if (is_file($filename) && self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $file))
									{
										$info = @stat($filename);
										if ($info === false)  continue;

										$options2 = array(
											"last_modified" => $info["mtime"],
											"extra_fields" => array()
										);

										// NTFS timestamps.
										ZipStreamWriter::AppendNTFSExtraField($options2["extra_fields"], $info["mtime"], $info["atime"], $info["ctime"]);

										if (!$windows)
										{
											// UNIX timestamps + uid/gid.
											ZipStreamWriter::AppendUNIXExtraField($options2["extra_fields"], $info["atime"], $info["mtime"], $info["uid"], $info["gid"]);

											$options2["unix_attrs"] = $info["mode"];
										}

										// For small files under 1MB, compress and output directly.
										if ($info["size"] <= 1048576)  $zip->AddFileFromString($path . "/" . $file, @file_get_contents($filename), $options2);
										else
										{
											$fp = @fopen($filename, "rb");

											if ($fp !== false)
											{
												$zip->OpenFile($path . "/" . $file, $options2);

												$size = $info["size"];
												while ($size)
												{
													$data = @fread($fp, ($size > 1048576 ? 1048576 : $size));
													if ($data == "")  break;

													$zip->AppendFileData($data);
													if ($zip->BytesAvailable() >= 65536)  echo $zip->Read();

													$size -= strlen($data);
												}

												$zip->CloseFile();

												fclose($fp);
											}
										}

										if ($zip->BytesAvailable() >= 65536)  echo $zip->Read();
									}
								}

								closedir($dir);
							}
						}
						else if (is_file($srcpath2))
						{
							if (!self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $path))  continue;

							$options2 = array(
								"last_modified" => $info["mtime"],
								"extra_fields" => array()
							);

							// NTFS timestamps.
							ZipStreamWriter::AppendNTFSExtraField($options2["extra_fields"], $info["mtime"], $info["atime"], $info["ctime"]);

							if (!$windows)
							{
								// UNIX timestamps + uid/gid.
								ZipStreamWriter::AppendUNIXExtraField($options2["extra_fields"], $info["atime"], $info["mtime"], $info["uid"], $info["gid"]);

								$options2["unix_attrs"] = $info["mode"];
							}

							// For small files under 1MB, compress and output directly.
							if ($info["size"] <= 1048576)  $zip->AddFileFromString($path, @file_get_contents($srcpath2), $options2);
							else
							{
								$fp = @fopen($srcpath2, "rb");

								if ($fp !== false)
								{
									$zip->OpenFile($path, $options2);

									$size = $info["size"];
									while ($size)
									{
										$data = @fread($fp, ($size > 1048576 ? 1048576 : $size));
										if ($data == "")  break;

										$zip->AppendFileData($data);
										if ($zip->BytesAvailable() >= 65536)  echo $zip->Read();

										$size -= strlen($data);
									}

									$zip->CloseFile();

									fclose($fp);
								}
							}

							if ($zip->BytesAvailable() >= 65536)  echo $zip->Read();
						}
					}

					$zip->Finalize();

					echo $zip->Read();
				}

				exit();
			}

			return $result;
		}

		// Copy initialization.
		protected static function ProcessCopyInitAction(&$options)
		{
			$srcpath = self::GetSanitizedPath($options["base_dir"], "srcpath", $options["dot_folders"]);
			$destpath = self::GetSanitizedPath($options["base_dir"], "destpath", $options["dot_folders"]);

			$srcids = self::GetRequestVar("srcids");
			if ($srcids !== false)  $srcids = @json_decode($srcids, true);

			if (!isset($options["copy"]) || !$options["copy"])  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "copy_not_allowed");
			else if ($srcpath === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid source path specified."), "errorcode" => "invalid_srcpath");
			else if ($destpath === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid destination path specified."), "errorcode" => "invalid_destpath");
			else if (self::IsRecycleBin($destpath, $options))  $result = array("success" => false, "error" => self::FETranslate("Cannot copy files to the recycling bin."), "errorcode" => "access_denied");
			else if (!is_array($srcids))  $result = array("success" => false, "error" => self::FETranslate("Invalid source IDs specified."), "errorcode" => "invalid_srcids");
			else
			{
				$depth = self::GetPathDepth($destpath, $options["base_dir"]);

				if ($depth < $options["protect_depth"])  $result = array("success" => false, "error" => self::FETranslate("The destination folder cannot be modified."), "errorcode" => "access_denied");
				else
				{
					header("Content-Type: application/json");

					@set_time_limit(0);

					// Scan the items for an overwrite count.
					$ts = time();
					$opnum = 0;
					$overwrite = 0;
					$pathstack = array();
					foreach ($srcids as $id)
					{
						$id = self::CleanFilename($id);

						if ($id !== false)  $pathstack[] = $id;
					}
					$origpathstack = $pathstack;

					while (count($pathstack))
					{
						// Process files first.
						$y = count($pathstack);
						for ($x = 0; $x < $y && is_dir($srcpath . "/" . $pathstack[$x]); $x++);
						if ($x >= $y)  $x = 0;

						$path = array_splice($pathstack, $x, 1);
						$path = $path[0];
						$srcpath2 = $srcpath . "/" . $path;
						$destpath2 = $destpath . "/" . $path;

						// Skip if recursion/recycle bin detected.
						if ($srcpath2 === $destpath || self::IsRecycleBin($destpath2, $options))  continue;

						if (is_dir($srcpath2))
						{
							if (file_exists($destpath2) && $srcpath2 !== $destpath2)
							{
								$dir = @opendir($srcpath2);
								if ($dir)
								{
									while (($file = readdir($dir)) !== false)
									{
										if ($file === "." || $file === "..")  continue;

										$pathstack[] = $path . "/" . $file;
									}

									closedir($dir);
								}
							}
						}
						else if (is_file($srcpath2))
						{
							if (file_exists($destpath2) && $srcpath2 !== $destpath2)  $overwrite++;
						}

						$opnum++;
						if ($opnum % 250 == 0)
						{
							$ts2 = time();
							if ($ts !== $ts2)
							{
								echo " ";

								$ts = $ts2;
							}
						}
					}

					// Generate and write information to disk.
					$copykey = "fe_copy_" . date("Y-m-d_H-i-s") . "_" . bin2hex(random_bytes(16));
					$opdata = array(
						"action" => "copy",
						"multi" => ($options["action"] === $options["requestprefix"] . "copy_init"),
						"totalbytes" => 0,
						"itemsdone" => 0,
						"faileditems" => 0,
						"srcpath" => $srcpath,
						"destpath" => $destpath,
						"copykey" => "fe_copy_" . date("Y-m-d_H-i-s"),
						"finalentries" => array(),
						"pathmap" => array(),
						"pathstack" => $origpathstack
					);

					file_put_contents($options["temp_dir"] . "/" . $copykey . ".dat", json_encode($opdata, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT));

					$_POST["copykey"] = $copykey;

					$result = array(
						"success" => true,
						"copykey" => $copykey,
						"overwrite" => $overwrite
					);
				}
			}

			return $result;
		}

		// Copy.
		protected static function ProcessCopyAction(&$options)
		{
			$copykey = self::GetSanitizedFile("copykey");
			$currpath = self::GetSanitizedPath($options["base_dir"], "currpath", $options["dot_folders"]);

			if ($copykey !== false)
			{
				$copykeyfile = $options["temp_dir"] . "/" . $copykey . ".dat";

				$opdata = @json_decode(file_get_contents($copykeyfile), true);
			}

			if (!isset($options["copy"]) || !$options["copy"])  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "copy_not_allowed");
			else if ($copykey === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid copy key specified.  Expected a string."), "errorcode" => "invalid_copykey");
			else if (!is_array($opdata) || !isset($opdata["action"]) || $opdata["action"] !== "copy")  $result = array("success" => false, "error" => self::FETranslate("Copy key does not map to a valid operations data file."), "errorcode" => "invalid_copykey");
			else
			{
				header("Content-Type: application/json");

				@set_time_limit(0);

				// Only copy allowed file extensions.
				if (is_bool($options["allowed_exts"]))  $allowedexts = $options["allowed_exts"];
				else  $allowedexts = self::ExtractAllowedExtensions($options["allowed_exts"]);

				// Copy folders and files.
				$ts = time();
				$srcpath = $opdata["srcpath"];
				$destpath = $opdata["destpath"];
				$depth = self::GetPathDepth($destpath, $options["base_dir"]);
				if ($currpath !== false)  $currdepth = self::GetPathDepth($currpath, $options["base_dir"]);
				$hasdir = false;
				$currentries = array();

				while (count($opdata["pathstack"]))
				{
					// Process files first.
					$y = count($opdata["pathstack"]);
					for ($x = 0; $x < $y && is_dir($srcpath . "/" . $opdata["pathstack"][$x]); $x++)
					{
						$hasdir = true;
					}
					if ($x >= $y)  $x = 0;

					$path = array_splice($opdata["pathstack"], $x, 1);
					$path = $path[0];
					$srcpath2 = $srcpath . "/" . $path;

					if ($srcpath !== $destpath)  $destpath2 = $destpath . "/" . $path;
					else
					{
						// Handle case where source and destination are the same.
						// Change the destination directory or file.
						$pos = strpos($path, "/");
						$path2 = ($pos !== false ? substr($path, 0, $pos) : $path);

						if (isset($opdata["pathmap"][$destpath . "/" . $path2]))  $destpath2 = $opdata["pathmap"][$destpath . "/" . $path2] . substr($path, strlen($path2));
						else
						{
							if (is_dir($srcpath . "/" . $path2))
							{
								$num = 1;
								do
								{
									$path3 = $path2 . self::FETranslate(" - Copy" . ($num > 1 ? " %u" : ""), $num);
									$num++;
								} while (file_exists($destpath . "/" . $path3));

								$opdata["pathmap"][$destpath . "/" . $path2] = $destpath . "/" . $path3;

								$destpath2 = $destpath . "/" . $path3 . substr($path, strlen($path2));
							}
							else if (is_file($srcpath . "/" . $path2))
							{
								$pos = strpos($path2, ".");
								if ($pos === false)
								{
									$path3 = $path2;
									$ext = "";
								}
								else
								{
									$path3 = substr($path2, 0, $pos);
									$ext = substr($path2, $pos);
								}

								$num = 1;
								do
								{
									$path4 = $path3 . self::FETranslate(" - Copy" . ($num > 1 ? " %u" : ""), $num) . $ext;
									$num++;
								} while (file_exists($destpath . "/" . $path4));

								$destpath2 = $destpath . "/" . $path4;
							}
							else
							{
								continue;
							}
						}
					}

					// Skip if recursion/recycle bin detected.
					if ($srcpath2 === $destpath || self::IsRecycleBin($destpath2, $options))  continue;

					if (is_dir($srcpath2))
					{
						// Create the destination directory.
						if (is_dir($destpath2))
						{
							if (strncmp($destpath2 . "/", $destpath . "/", strlen($destpath) + 1) == 0 && strpos($destpath2, "/", strlen($destpath) + 1) === false)
							{
								$entry = self::BuildEntry($destpath, substr($destpath2, strlen($destpath) + 1), "folder", $depth, $options);
								if ($entry !== false)  $opdata["finalentries"][] = $entry;
							}
						}
						else if (!@mkdir($destpath2, 0775, true))
						{
							$opdata["faileditems"]++;

							$opdata["lastfailed"] = "mkdir: " . $destpath2;
							$opdata["lastdirfailed"] = $destpath2;
						}
						else
						{
							$opdata["itemsdone"]++;

							if (strncmp($destpath2 . "/", $destpath . "/", strlen($destpath) + 1) == 0 && strpos($destpath2, "/", strlen($destpath) + 1) === false)
							{
								$entry = self::BuildEntry($destpath, substr($destpath2, strlen($destpath) + 1), "folder", $depth, $options);
								if ($entry !== false)  $opdata["finalentries"][] = $entry;
							}

							if ($currpath !== false && strncmp($destpath2 . "/", $currpath . "/", strlen($currpath) + 1) == 0 && strpos($destpath2, "/", strlen($currpath) + 1) === false)
							{
								$entry = self::BuildEntry($currpath, substr($destpath2, strlen($currpath) + 1), "folder", $currdepth, $options);
								if ($entry !== false)  $currentries[] = $entry;
							}

							$opdata["lastsuccess"] = "mkdir: " . $destpath2;
						}

						$dir = @opendir($srcpath2);
						if ($dir)
						{
							while (($file = readdir($dir)) !== false)
							{
								if ($file === "." || $file === "..")  continue;

								$opdata["pathstack"][] = $path . "/" . $file;
							}

							closedir($dir);
						}
					}
					else if (is_file($srcpath2))
					{
						// Check the file extension.
						$pos = strrpos($destpath2, "/");
						$file = substr($destpath2, $pos + 1);
						if (!self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $file))  continue;

						// Create a backup in the recycle bin on overwrite.
						if (file_exists($destpath2) && isset($options["recycle_to"]) && is_string($options["recycle_to"]))
						{
							$recyclepath = $options["base_dir"] . "/" . $options["recycle_to"] . "/" . $opdata["copykey"] . substr($destpath2, strlen($destpath), strlen($destpath2) - strlen($destpath) - strlen($file) - 1);
							@mkdir($recyclepath, 0775, true);

							@rename($destpath2, $recyclepath . "/" . $file);
						}

						// Copy the file.
						if (!@copy($srcpath2, $destpath2))
						{
							$opdata["faileditems"]++;

							$opdata["lastfailed"] = "copy: " . $destpath2;
							$opdata["lastfilefailed"] = $destpath2;
						}
						else
						{
							$opdata["itemsdone"]++;
							$opdata["totalbytes"] += filesize($destpath2);

							if (strncmp($destpath2 . "/", $destpath . "/", strlen($destpath) + 1) == 0 && strpos($destpath2, "/", strlen($destpath) + 1) === false)
							{
								$entry = self::BuildEntry($destpath, substr($destpath2, strlen($destpath) + 1), "file", $depth, $options);
								if ($entry !== false)  $opdata["finalentries"][] = $entry;
							}

							if ($currpath !== false && strncmp($destpath2 . "/", $currpath . "/", strlen($currpath) + 1) == 0 && strpos($destpath2, "/", strlen($currpath) + 1) === false)
							{
								$entry = self::BuildEntry($currpath, substr($destpath2, strlen($currpath) + 1), "file", $currdepth, $options);
								if ($entry !== false)  $currentries[] = $entry;
							}
						}
					}

					$ts2 = time();
					if ($opdata["multi"])
					{
						// Exit after a few seconds.
						if ($ts < $ts2 - 2)  break;
					}
					else if ($ts !== $ts2)
					{
						// Echo out a space every second to keep the connection alive.
						echo " ";

						$ts = $ts2;
					}
				}

				$result = array(
					"success" => true,
					"copykey" => $copykey,
					"totalbytes" => $opdata["totalbytes"],
					"queueditems" => count($opdata["pathstack"]),
					"queuesizeunknown" => ($hasdir && count($opdata["pathstack"])),
					"itemsdone" => $opdata["itemsdone"],
					"faileditems" => $opdata["faileditems"],
					"currentries" => $currentries
				);

				if (!count($opdata["pathstack"]))  $result["finalentries"] = $opdata["finalentries"];

				if (count($opdata["pathstack"]))  @file_put_contents($copykeyfile, json_encode($opdata, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT));
				else  @unlink($copykeyfile);
			}

			return $result;
		}

		// Move.
		protected static function ProcessMoveAction(&$options)
		{
			$srcpath = self::GetSanitizedPath($options["base_dir"], "srcpath", $options["dot_folders"]);
			$destpath = self::GetSanitizedPath($options["base_dir"], "destpath", $options["dot_folders"]);

			$srcids = self::GetRequestVar("srcids");
			if ($srcids !== false)  $srcids = @json_decode($srcids, true);

			if (!isset($options["move"]) || !$options["move"])  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "move_not_allowed");
			else if ($srcpath === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid source path specified."), "errorcode" => "invalid_srcpath");
			else if ($destpath === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid destination path specified."), "errorcode" => "invalid_destpath");
			else if (self::IsRecycleBin($destpath, $options))  $result = array("success" => false, "error" => self::FETranslate("Cannot move files to the recycling bin."), "errorcode" => "access_denied");
			else if (!is_array($srcids))  $result = array("success" => false, "error" => self::FETranslate("Invalid source IDs specified."), "errorcode" => "invalid_srcids");
			else
			{
				$depth = self::GetPathDepth($destpath, $options["base_dir"]);

				if ($depth < $options["protect_depth"])  $result = array("success" => false, "error" => self::FETranslate("The destination folder cannot be modified."), "errorcode" => "access_denied");
				else
				{
					// Only move allowed file extensions.
					if (is_bool($options["allowed_exts"]))  $allowedexts = $options["allowed_exts"];
					else  $allowedexts = self::ExtractAllowedExtensions($options["allowed_exts"]);

					$entries = array();

					foreach ($srcids as $id)
					{
						$file = self::CleanFilename($id);

						if ($file !== false)
						{
							if (is_dir($srcpath . "/" . $file))
							{
								if (@rename($srcpath . "/" . $file, $destpath . "/" . $file))
								{
									$entry = self::BuildEntry($destpath, $file, "folder", $depth, $options);
									if ($entry !== false)  $entries[] = $entry;
								}
							}
							else if (is_file($srcpath . "/" . $file))
							{
								// Check the file extension.
								if (!self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $file))  continue;

								if (@rename($srcpath . "/" . $file, $destpath . "/" . $file))
								{
									$entry = self::BuildEntry($destpath, $file, "file", $depth, $options);
									if ($entry !== false)  $entries[] = $entry;
								}
							}
						}
					}

					$result = array(
						"success" => true,
						"entries" => $entries
					);
				}
			}

			return $result;
		}

		// Recycle.
		protected static function ProcessRecycleAction(&$options)
		{
			$srcpath = self::GetSanitizedPath($options["base_dir"], "path", $options["dot_folders"]);

			$ids = self::GetRequestVar("ids");
			if ($ids !== false)  $ids = @json_decode($ids, true);

			if (!isset($options["recycle"]) || !$options["recycle"])  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "recycle_not_allowed");
			else if (!isset($options["recycle_to"]) || !is_string($options["recycle_to"]))  $result = array("success" => false, "error" => self::FETranslate("Recycling not configured properly."), "errorcode" => "invalid_server_config");
			else if ($srcpath === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid path specified."), "errorcode" => "invalid_path");
			else if (self::IsRecycleBin($srcpath, $options))  $result = array("success" => false, "error" => self::FETranslate("Cannot recycle files already in the recycling bin."), "errorcode" => "access_denied");
			else if (!is_array($ids))  $result = array("success" => false, "error" => self::FETranslate("Invalid IDs specified."), "errorcode" => "invalid_ids");
			else
			{
				$depth = self::GetPathDepth($srcpath, $options["base_dir"]);

				if ($depth < $options["protect_depth"])  $result = array("success" => false, "error" => self::FETranslate("The items in the current folder cannot be recycled."), "errorcode" => "access_denied");
				else
				{
					// Only recycle allowed file extensions.
					if (is_bool($options["allowed_exts"]))  $allowedexts = $options["allowed_exts"];
					else  $allowedexts = self::ExtractAllowedExtensions($options["allowed_exts"]);

					$destpath = $options["base_dir"] . "/" . $options["recycle_to"] . "/" . date("Y-m-d_H-i-s");
					@mkdir($destpath, 0775, true);

					foreach ($ids as $id)
					{
						$file = self::CleanFilename($id);

						if ($file !== false)
						{
							if (is_dir($srcpath . "/" . $file))
							{
								@rename($srcpath . "/" . $file, $destpath . "/" . $file);
							}
							else if (is_file($srcpath . "/" . $file))
							{
								// Check the file extension.
								if (!self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $file))  continue;

								@rename($srcpath . "/" . $file, $destpath . "/" . $file);
							}
						}
					}

					$result = array(
						"success" => true
					);
				}
			}

			return $result;
		}

		// Delete.
		protected static function ProcessDeleteAction(&$options)
		{
			$srcpath = self::GetSanitizedPath($options["base_dir"], "path", $options["dot_folders"]);

			$ids = self::GetRequestVar("ids");
			if ($ids !== false)  $ids = @json_decode($ids, true);

			if (!isset($options["delete"]) || !$options["delete"])  $result = array("success" => false, "error" => self::FETranslate("Operation denied."), "errorcode" => "delete_not_allowed");
			else if ($srcpath === false)  $result = array("success" => false, "error" => self::FETranslate("Invalid path specified."), "errorcode" => "invalid_path");
			else if (self::IsRecycleBin($srcpath, $options))  $result = array("success" => false, "error" => self::FETranslate("Cannot delete files in the recycling bin."), "errorcode" => "access_denied");
			else if (!is_array($ids))  $result = array("success" => false, "error" => self::FETranslate("Invalid IDs specified."), "errorcode" => "invalid_ids");
			else
			{
				$depth = self::GetPathDepth($srcpath, $options["base_dir"]);

				if ($depth < $options["protect_depth"])  $result = array("success" => false, "error" => self::FETranslate("The items in the current folder cannot be deleted."), "errorcode" => "access_denied");
				else
				{
					// Only delete allowed file extensions.
					if (is_bool($options["allowed_exts"]))  $allowedexts = $options["allowed_exts"];
					else  $allowedexts = self::ExtractAllowedExtensions($options["allowed_exts"]);

					header("Content-Type: application/json");

					@set_time_limit(0);

					$ts = time();
					$pathstack = array();
					foreach ($ids as $id)
					{
						$id = self::CleanFilename($id);

						if ($id !== false)  $pathstack[] = $id;
					}

					while (count($pathstack))
					{
						$path = array_shift($pathstack);
						$srcpath2 = $srcpath . "/" . $path;

						// Skip if recycle bin detected.
						if (self::IsRecycleBin($srcpath2, $options))  continue;

						if (is_dir($srcpath2))
						{
							$dir = @opendir($srcpath2);
							if ($dir)
							{
								while (($file = readdir($dir)) !== false)
								{
									if ($file === "." || $file === "..")  continue;

									$filename = $srcpath2 . "/" . $file;

									if (is_dir($filename))  $pathstack[] = $path . "/" . $file;
									else if (is_file($filename) && self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $file))  @unlink($filename);
								}

								closedir($dir);

								while (@rmdir($srcpath2))
								{
									$pos = strrpos($srcpath2, "/");
									if ($pos === false)  break;

									$srcpath2 = substr($srcpath2, 0, $pos);
								}
							}
						}
						else if (is_file($srcpath2))
						{
							if (self::HasAllowedExt($allowedexts, $options["allow_empty_ext"], $path))  @unlink($srcpath2);
						}

						$ts2 = time();
						if ($ts !== $ts2)
						{
							echo " ";

							$ts = $ts2;
						}
					}

					$result = array(
						"success" => true
					);
				}
			}

			return $result;
		}

		public static function HandleActions($requestvar, $requestprefix, $basedir, $options)
		{
			$action = self::GetRequestVar($requestvar);
			if ($action === false)  return false;

			if (!is_dir($basedir))  return array("success" => false, "error" => self::FETranslate("Supplied base directory does not exist."), "errorcode" => "invalid_base_dir");

			// Normalize options.
			$options["action"] = $action;
			$options["requestprefix"] = $requestprefix;
			$options["base_dir"] = str_replace("\\", "/", realpath($basedir));

			if (isset($options["base_url"]))  $options["base_url"] = rtrim($options["base_url"], "/");

			if (!isset($options["protect_depth"]))  $options["protect_depth"] = 0;
			if (!isset($options["allowed_exts"]))  $options["allowed_exts"] = true;
			if (!isset($options["allow_empty_ext"]))  $options["allow_empty_ext"] = true;
			if (!isset($options["dot_folders"]))  $options["dot_folders"] = false;

			if (isset($options["thumbs_dir"]))
			{
				if (!is_dir($options["thumbs_dir"]) || !isset($options["thumbs_url"]))  unset($options["thumbs_dir"]);
				else
				{
					$options["thumbs_dir"] = rtrim(str_replace("\\", "/", $options["thumbs_dir"]), "/");
					$options["thumbs_url"] = rtrim($options["thumbs_url"], "/");
				}
			}

			$options["started"] = time();

			$os = php_uname("s");
			$windows = (strtoupper(substr($os, 0, 3)) == "WIN");

			$options["windows"] = $windows;

			// Process various actions.
			if ($action === $requestprefix . "refresh")  $result = self::ProcessRefreshAction($options);
			else if ($action === $requestprefix . "thumbnail")  $result = self::ProcessThumnailAction($options);
			else if ($action === $requestprefix . "rename")  $result = self::ProcessRenameAction($options);
			else if ($action === $requestprefix . "file_info")  $result = self::ProcessFileInfoAction($options);
			else if ($action === $requestprefix . "load_file")  $result = self::ProcessLoadFileAction($options);
			else if ($action === $requestprefix . "save_file")  $result = self::ProcessSaveFileAction($options);
			else if ($action === $requestprefix . "new_folder")  $result = self::ProcessNewFolderAction($options);
			else if ($action === $requestprefix . "new_file")  $result = self::ProcessNewFileAction($options);
			else if ($action === $requestprefix . "upload_init" || $action === $requestprefix . "upload")  $result = self::ProcessUploadAction($options);
			else if ($action === $requestprefix . "download")  $result = self::ProcessDownloadAction($options);
			else if ($action === $requestprefix . "copy_init" || $action === $requestprefix . "copy")
			{
				// Copy is split into two parts:  copy_init and copy.
				if ($action === $requestprefix . "copy_init" || ($action === $requestprefix . "copy" && self::GetRequestVar("copykey") === false))  $result = self::ProcessCopyInitAction($options);

				if ($action === $requestprefix . "copy")  $result = self::ProcessCopyAction($options);
			}
			else if ($action === $requestprefix . "move")  $result = self::ProcessMoveAction($options);
			else if ($action === $requestprefix . "recycle")  $result = self::ProcessRecycleAction($options);
			else if ($action === $requestprefix . "delete")  $result = self::ProcessDeleteAction($options);
			else  $result = false;

			// Dump response to network.
			if ($result !== false)
			{
				if (!headers_sent())  header("Content-Type: application/json");

				echo json_encode($result, JSON_UNESCAPED_SLASHES);

				exit();
			}

			return false;
		}

		public static function FETranslate()
		{
			$args = func_get_args();
			if (!count($args))  return "";

			return call_user_func_array((defined("CS_TRANSLATE_FUNC") && function_exists(CS_TRANSLATE_FUNC) ? CS_TRANSLATE_FUNC : "sprintf"), $args);
		}
	}
?>