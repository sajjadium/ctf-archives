<?php
	// ZIP file stream writer.  Uses DeflateStream and CRC32Stream.
	// (C) 2020 CubicleSoft.  All Rights Reserved.

	// NOTE:  There is no such thing as a ZipStreamReader.  ZIP files have to be complete in order to read them.
	class ZipStreamWriter
	{
		protected $open, $outdata, $outdatasize, $disknum, $centraldirs, $currdir, $currcrc32, $currds;

		// Made by OS options.
		const MADE_BY_MSDOS = 0;
		const MADE_BY_AMIGA = 1;
		const MADE_BY_OPENVMS = 2;
		const MADE_BY_UNIX = 3;
		const MADE_BY_VM_CMS = 4;
		const MADE_BY_ATARI_ST = 5;
		const MADE_BY_OS2 = 6;
		const MADE_BY_MAC = 7;
		const MADE_BY_ZSYSTEM = 8;
		const MADE_BY_CPM = 9;
		const MADE_BY_WIN_NTFS = 10;
		const MADE_BY_MVS = 11;
		const MADE_BY_VSE = 12;
		const MADE_BY_ACORN_RISC = 13;
		const MADE_BY_VFAT = 14;
		const MADE_BY_ALT_MVS = 15;
		const MADE_BY_BEOS = 16;
		const MADE_BY_TANDEM = 17;
		const MADE_BY_OS400 = 18;
		const MADE_BY_MAC_OSX = 19;


		// General-purpose bit flags.
		const FLAG_NORMAL = 0x0000;
		const FLAG_ENCRYPTED = 0x0001;

		const FLAG_IMPLODE_4K = 0x0000;
		const FLAG_IMPLODE_8K = 0x0002;
		const FLAG_IMPLODE_2_SHANNON_FANO = 0x0000;
		const FLAG_IMPLODE_3_SHANNON_FANO = 0x0004;
		const FLAG_DEFLATE_NORMAL = 0x0000;
		const FLAG_DEFLATE_MAXIMUM = 0x0002;
		const FLAG_DEFLATE_FAST = 0x0004;
		const FLAG_DEFLATE_SUPER_FAST = 0x0006;
		const FLAG_LZMA_NO_EOS = 0x0000;
		const FLAG_LZMA_EOS = 0x0002;

		const FLAG_USE_DATA_DESCRIPTOR = 0x0008;

		const FLAG_PATCHED = 0x0020;
		const FLAG_STRONG_ENCRYPTION = 0x0041;
		// Bit flags 7-10 are unused.
		const FLAG_UTF8 = 0x0800;

		const FLAG_RESERVED_ENHANCED_COMPRESSION = 0x1000;  // Reserved.
		const FLAG_MASKED_VALUES = 0x2000;
		const FLAG_RESERVED_ALT_STREAMS = 0x4000;  // Reserved.
		const FLAG_RESERVED_15 = 0x8000;  // Reserved.


		// Common compression methods.
		const COMPRESS_METHOD_STORE = 0;  // Uncompressed.
		const COMPRESS_METHOD_DEFLATE = 8;  // Standard compression.

		// Rarer/deprecated compression methods.  Not implemented in this library.
		const COMPRESS_METHOD_SHRINK = 1;  // Deprecated.
		const COMPRESS_METHOD_REDUCE_1 = 2;  // Deprecated.
		const COMPRESS_METHOD_REDUCE_2 = 3;  // Deprecated.
		const COMPRESS_METHOD_REDUCE_3 = 4;  // Deprecated.
		const COMPRESS_METHOD_REDUCE_4 = 5;  // Deprecated.
		const COMPRESS_METHOD_IMPLODE = 6;  // Deprecated.
		const COMPRESS_METHOD_RESERVED_TOKENIZE = 7;  // Reserved.
		const COMPRESS_METHOD_DEFLATE64 = 9;
		const COMPRESS_METHOD_IBM_TERSE_OLD = 10;
		const COMPRESS_METHOD_RESERVED_11 = 11;  // Reserved.
		const COMPRESS_METHOD_BZIP2 = 12;
		const COMPRESS_METHOD_RESERVED_13 = 13;  // Reserved.
		const COMPRESS_METHOD_LZMA = 14;
		const COMPRESS_METHOD_RESERVED_15 = 15;  // Reserved.
		const COMPRESS_METHOD_IBM_ZOS_CMPSC = 16;
		const COMPRESS_METHOD_RESERVED_17 = 17;  // Reserved.
		const COMPRESS_METHOD_IBM_TERSE_NEW = 18;
		const COMPRESS_METHOD_IBM_LZ77 = 19;
		const COMPRESS_METHOD_ZSTANDARD = 20;
		const COMPRESS_METHOD_JPEG = 96;
		const COMPRESS_METHOD_WAVPACK = 97;
		const COMPRESS_METHOD_PPMD = 98;
		const COMPRESS_METHOD_AEX_MARKER = 99;


		// Extra information fields.
		const EXTRA_FIELD_ZIP64 = 0x0001;
		const EXTRA_FIELD_OS2 = 0x0009;
		const EXTRA_FIELD_NTFS = 0x000A;
		const EXTRA_FIELD_NTFS_TAG_TIMESTAMP = 0x0001;
		const EXTRA_FIELD_UNIX = 0x000D;

		// Not implemented in this class.
		const EXTRA_FIELD_AV_INFO = 0x0007;
		const EXTRA_FIELD_RESERVED_EXTENDED_LANG = 0x0008;
		const EXTRA_FIELD_OPENVMS = 0x000C;
		const EXTRA_FIELD_RESERVED_ALT_STREAMS = 0X000E;  // Reserved.
		const EXTRA_FIELD_PATCH = 0x000F;  // Supposedly a proprietary, patented feature.

		// Encryption constants are defined but encryption support is not implemented in this class.
		const EXTRA_FIELD_PKCS7_STORE = 0x0014;
		const EXTRA_FIELD_X509_FILE = 0x0015;
		const EXTRA_FIELD_X509_CENTRAL_DIR = 0x0016;
		const EXTRA_FIELD_STRONG_ENCRYPT_HEADER = 0x0017;
		const EXTRA_FIELD_RECORD_MANAGEMENT = 0x0018;
		const EXTRA_FIELD_PKCS7_RECIPIENT_LIST = 0x0019;
		const EXTRA_FIELD_RESERVED_TIMESTAMP = 0x0020;
		const EXTRA_FIELD_POLICY_DECRYPT_KEY = 0x0021;
		const EXTRA_FIELD_SMARTCRYPT_KEY_PROVIDER = 0x0022;
		const EXTRA_FIELD_SMARTCRYPT_POLICY_KEY_DATA = 0x0023;
		const EXTRA_FIELD_IBM_ATTRS_UNCOMPRESSED = 0x0065;
		const EXTRA_FIELD_IBM_ATTRS_COMPRESSED = 0x0066;
		const EXTRA_FIELD_RESERVED_POSZIP = 0x4690;

		// Third-party extra information fields.  Not implemented in this class.
		const EXTRA_FIELD_3RD_PARTY_MAC = 0x07C8;
		const EXTRA_FIELD_ZIPIT_MAC_LONG = 0x2605;
		const EXTRA_FIELD_ZIPIT_MAC_SHORT_FILE = 0x2705;
		const EXTRA_FIELD_ZIPIT_MAC_SHORT_DIR = 0x2805;
		const EXTRA_FIELD_INFO_ZIP_MAC = 0x334D;
		const EXTRA_FIELD_ACORN_SPARK = 0x4341;
		const EXTRA_FIELD_WIN_NT_ACL = 0x4453;  // Binary ACL.
		const EXTRA_FIELD_VM_CMS = 0x4704;
		const EXTRA_FIELD_MVS = 0x470F;
		const EXTRA_FIELD_FWKCS_MD5 = 0x4B46;
		const EXTRA_FIELD_OS2_ACL = 0x4C41;  // Text ACL.
		const EXTRA_FIELD_INFO_ZIP_OPENVMS = 0x4D49;
		const EXTRA_FIELD_XCEED_ORIG_LOCATION = 0x4F4C;
		const EXTRA_FIELD_AOS_VS_ACL = 0x5356;  // ACL.
		const EXTRA_FIELD_EXTENEDED_TIMESTAMP = 0x5455;
		const EXTRA_FIELD_XCEED_UNICODE = 0x554E;
		const EXTRA_FIELD_INFO_ZIP_UNIX_OLD = 0x5855;  // Also OS/2, NT, etc.
		const EXTRA_FIELD_INFO_ZIP_UNICODE_COMMENT = 0x6375;  // Prefer FLAG_UTF8.
		const EXTRA_FIELD_BEOS_BEBOX = 0x6542;
		const EXTRA_FIELD_INFO_ZIP_UNICODE_PATH = 0x7075;  // Prefer FLAG_UTF8.
		const EXTRA_FIELD_ASI_UNIX = 0x756E;
		const EXTRA_FIELD_INFO_ZIP_UNIX_NEW = 0x7855;
		const EXTRA_FIELD_DATA_STREAM_ALIGN = 0xA11E;  // Apache Commons-Compress.
		const EXTRA_FIELD_MICROSOFT_OPEN_PACKAGING_GROWTH = 0xA220;
		const EXTRA_FIELD_SMS_QDOS = 0xFD4A;
		const EXTRA_FIELD_AEX_ENCRYPTION_STRUCTURE = 0x9901;
		const EXTRA_FIELD_UNKNOWN_9902 = 0x9902;  // Unknown.


		// File attributes.
		const FILE_ATTRIBUTE_MSDOS_READONLY = 0x00000001;
		const FILE_ATTRIBUTE_MSDOS_HIDDEN = 0x00000002;
		const FILE_ATTRIBUTE_MSDOS_SYSTEM = 0x00000004;
		const FILE_ATTRIBUTE_MSDOS_DIRECTORY = 0x00000010;
		const FILE_ATTRIBUTE_MSDOS_ARCHIVE = 0x00000020;
		const FILE_ATTRIBUTE_MSDOS_DEVICE = 0x00000040;  // Reserved for system use.
		const FILE_ATTRIBUTE_MSDOS_NORMAL = 0x00000080;
		const FILE_ATTRIBUTE_MSDOS_SYMLINK = 0x00000400;  // FILE_ATTRIBUTE_REPARSE_POINT (it's real name) is not really supported by ZIP programs but would be a really good idea if they did!

		const FILE_ATTRIBUTE_UNIX_DEVICE_NAMED_PIPE = 0x10000000;
		const FILE_ATTRIBUTE_UNIX_DEVICE_CHAR_SPECIAL = 0x20000000;
		const FILE_ATTRIBUTE_UNIX_DEVICE_DIRECTORY = 0x40000000;
		const FILE_ATTRIBUTE_UNIX_DEVICE_BLOCK_SPECIAL = 0x60000000;
		const FILE_ATTRIBUTE_UNIX_DEVICE_REGULAR = 0x80000000;
		const FILE_ATTRIBUTE_UNIX_DEVICE_SYMLINK = 0xA0000000;
		const FILE_ATTRIBUTE_UNIX_DEVICE_SOCKET = 0xC0000000;

		const FILE_ATTRIBUTE_UNIX_SETUID = 0x08000000;
		const FILE_ATTRIBUTE_UNIX_SETGID = 0x04000000;
		const FILE_ATTRIBUTE_UNIX_STICKY = 0x02000000;
		const FILE_ATTRIBUTE_UNIX_OWNER_READ = 0x01000000;
		const FILE_ATTRIBUTE_UNIX_OWNER_WRITE = 0x00800000;
		const FILE_ATTRIBUTE_UNIX_OWNER_EXECUTE = 0x00400000;
		const FILE_ATTRIBUTE_UNIX_GROUP_READ = 0x00200000;
		const FILE_ATTRIBUTE_UNIX_GROUP_WRITE = 0x00100000;
		const FILE_ATTRIBUTE_UNIX_GROUP_EXECUTE = 0x00080000;
		const FILE_ATTRIBUTE_UNIX_OTHER_READ = 0x00040000;
		const FILE_ATTRIBUTE_UNIX_OTHER_WRITE = 0x00020000;
		const FILE_ATTRIBUTE_UNIX_OTHER_EXECUTE = 0x00010000;


		public function __construct()
		{
			$this->open = false;
		}

		public static function IsDeflateSupported()
		{
			if (!class_exists("DeflateStream", false))  require_once str_replace("\\", "/", dirname(__FILE__)) . "/deflate_stream.php";

			return DeflateStream::IsSupported();
		}

		public static function StartHTTPResponse($filename)
		{
			// Carefully clear out various PHP restrictions.
			@set_time_limit(0);

			@ob_clean();
			if (function_exists("apache_setenv"))  @apache_setenv("no-gzip", 1);
			@ini_set("zlib.output_compression", "Off");

			// Send the headers.
			header("Content-Type: application/octet-stream");
			header("Content-Disposition: attachment; filename=\"" . str_replace(array("\"", "'", "\\", "/", ";", "\r", "\n"), "_", $filename) . "\"");
			header("Pragma: no-cache");
			header("Cache-Control: no-cache, no-store");
		}

		public function Init()
		{
			if (!class_exists("CRC32Stream", false))  require_once str_replace("\\", "/", dirname(__FILE__)) . "/crc32_stream.php";
			if (!class_exists("DeflateStream", false))  require_once str_replace("\\", "/", dirname(__FILE__)) . "/deflate_stream.php";

			$this->outdata = "";
			$this->outdatasize = 0;
			$this->disknum = 0;
			$this->centraldirs = array();
			$this->currdir = false;
			$this->currcrc32 = false;
			$this->currds = false;

			$this->open = true;

			return true;
		}

		public function AddDirectory($path, $options = array())
		{
			if (!$this->open)  return false;

			// Close an open file.
			$this->CloseFile();

			$path = trim(str_replace("\\", "/", $path), "/") . "/";

			if (!isset($options["version_required"]) || $options["version_required"] < 2.0)  $options["version_required"] = 2.0;
			if (!isset($options["flags"]))  $options["flags"] = self::FLAG_NORMAL | self::FLAG_UTF8;
			if (!isset($options["last_modified"]))  $options["last_modified"] = time();

			unset($options["64bit"]);
			unset($options["crc32"]);
			unset($options["uncompressed_size"]);
			unset($options["compressed_size"]);

			$options["bytes_left"] = 0;
			$options["filename"] = $path;
			$options["disk_start_num"] = $this->disknum;
			$options["header_offset"] = $this->outdatasize;

			$this->currdir = self::InitCentralDirHeader($options, self::FILE_ATTRIBUTE_MSDOS_DIRECTORY);

			// Write the directory.
			$this->WriteLocalFileHeader();

			return $this->CloseFile();
		}

		// For smaller files, it is possible to add the whole thing at once.
		public function AddFileFromString($filename, $data, $options = array(), $compresslevel = -1)
		{
			if (!$this->open || !is_string($data))  return false;

			// Close an open file.
			$this->CloseFile();

			$deflatesupported = (isset($options["compress_method"]) && $options["compress_method"] === self::COMPRESS_METHOD_STORE ? false : DeflateStream::IsSupported());

			// Compress the data in advance.  If the compressed version ends up larger than the original, just store it instead.
			if ($deflatesupported)
			{
				$data2 = DeflateStream::Compress($data, $compresslevel);

				if (strlen($data) <= strlen($data2))
				{
					$deflatesupported = false;

					unset($data2);
				}
			}

			$filename = trim(str_replace("\\", "/", $filename), "/");

			if (!isset($options["version_required"]) || $options["version_required"] < 1.0)  $options["version_required"] = 1.0;
			if (!isset($options["flags"]))  $options["flags"] = ($deflatesupported ? self::FLAG_DEFLATE_NORMAL : self::FLAG_NORMAL) | self::FLAG_UTF8;
			if (!isset($options["last_modified"]))  $options["last_modified"] = time();

			$options["64bit"] = (strlen($data) < 0 || strlen($data) > 0x7FFFFFFF);

			$options["compress_method"] = ($deflatesupported ? self::COMPRESS_METHOD_DEFLATE : self::COMPRESS_METHOD_STORE);
			$options["crc32"] = crc32($data);
			$options["uncompressed_size"] = strlen($data);

			// Compress the data.
			if ($deflatesupported)  $data = $data2;

			$options["compressed_size"] = strlen($data);
			$options["bytes_left"] = 0;
			$options["filename"] = $filename;
			$options["disk_start_num"] = $this->disknum;
			$options["header_offset"] = $this->outdatasize;

			$this->currdir = self::InitCentralDirHeader($options);

			// Write the directory.
			$this->WriteLocalFileHeader();

			// Write the data.
			$this->outdata .= $data;
			$this->outdatasize += strlen($data);

			return $this->CloseFile();
		}

		public function OpenFile($filename, $options = array(), $compresslevel = -1)
		{
			if (!$this->open)  return false;

			// Close an open file.
			$this->CloseFile();

			// Initialize a bunch of options.
			$deflatesupported = (isset($options["compress_method"]) && $options["compress_method"] === self::COMPRESS_METHOD_STORE ? false : DeflateStream::IsSupported());

			$filename = trim(str_replace("\\", "/", $filename), "/");

			if (!isset($options["64bit"]))  $options["64bit"] = (isset($options["uncompressed_size"]) && ($options["uncompressed_size"] < 0 || $options["uncompressed_size"] > 0x7FFFFFFF));

			if (isset($options["uncompressed_size"]) && $options["uncompressed_size"] < 0)  unset($options["uncompressed_size"]);

			$minver = ($options["64bit"] ? 4.5 : 1.0);

			if (!isset($options["version_required"]) || $options["version_required"] < $minver)  $options["version_required"] = $minver;
			if (!isset($options["flags"]))  $options["flags"] = ($deflatesupported ? self::FLAG_DEFLATE_NORMAL : self::FLAG_NORMAL) | self::FLAG_UTF8;
			$options["flags"] |= self::FLAG_USE_DATA_DESCRIPTOR;
			if (!isset($options["last_modified"]))  $options["last_modified"] = time();

			$options["compress_method"] = ($deflatesupported ? self::COMPRESS_METHOD_DEFLATE : self::COMPRESS_METHOD_STORE);
			$options["crc32"] = 0;
			$options["compressed_size"] = 0;
			$options["filename"] = $filename;
			$options["disk_start_num"] = $this->disknum;
			$options["header_offset"] = $this->outdatasize;
			$options["bytes_left"] = (isset($options["uncompressed_size"]) ? $options["uncompressed_size"] : -1);

			$this->currdir = self::InitCentralDirHeader($options);

			if ($options["64bit"])  self::AppendZip64ExtraField($this->currdir["extra_fields"], (isset($options["uncompressed_size"]) ? $options["uncompressed_size"] : 0));

			// Write the file header.
			$this->WriteLocalFileHeader();

			// Set up data streams.
			$this->currcrc32 = new CRC32Stream();
			$this->currcrc32->Init();

			if ($deflatesupported)
			{
				$this->currds = new DeflateStream();
				$this->currds->Init("wb", $compresslevel);
			}

			return true;
		}

		public function AppendFileData($data)
		{
			if (!$this->open || $this->currdir === false)  return false;

			// Restrict the amount of data if the data size is known.
			if ($this->currdir["bytes_left"] > -1)
			{
				if (strlen($data) > $this->currdir["bytes_left"])  $data = substr($data, 0, $this->currdir["bytes_left"]);

				$this->currdir["bytes_left"] -= strlen($data);
			}
			else
			{
				$this->currdir["uncompressed_size"] += strlen($data);
			}

			$this->currcrc32->AddData($data);

			if ($this->currds === false)  $datasize = strlen($data);
			else
			{
				$this->currds->Write($data);
				$data = $this->currds->Read();
				$datasize = strlen($data);
			}

			$this->currdir["compressed_size"] += $datasize;

			$this->outdata .= $data;
			$this->outdatasize += $datasize;

			return true;
		}

		public function CloseFile()
		{
			if (!$this->open || $this->currdir === false)  return false;

			// Not writing all data is an error.
			if ($this->currdir["bytes_left"] > 0)  return false;

			// Finalize CRC-32 calculation.
			if ($this->currcrc32 !== false)
			{
				$this->currdir["crc32"] = $this->currcrc32->Finalize();
				$this->currcrc32 = false;
			}

			// Finalize compression.
			if ($this->currds !== false)
			{
				$this->currds->Finalize();
				$data = $this->currds->Read();
				$datasize = strlen($data);

				$this->currdir["compressed_size"] += $datasize;
				$this->outdata .= $data;
				$this->outdatasize += $datasize;

				$this->currds = false;
			}

			// Update Zip64 extra field, if set.
			foreach ($this->currdir["extra_fields"] as $num => $extrafield)
			{
				if (is_array($extrafield) && $extrafield["header_id"] === self::EXTRA_FIELD_ZIP64)
				{
					$extrafield["uncompressed_size"] = $this->currdir["uncompressed_size"];
					$extrafield["compressed_size"] = $this->currdir["compressed_size"];
					$extrafield["header_offset"] = $this->currdir["header_offset"];

					$this->currdir["extra_fields"][$num] = $extrafield;
				}
			}

			// Write out the data descriptor if necessary.
			$this->WriteDataDescriptor();

			// Append to the central directories.
			$this->centraldirs[] = $this->currdir;

			$this->currdir = false;

			return true;
		}

		public function Finalize($comment = "")
		{
			if (!$this->open)  return false;

			// Close an open file.
			$this->CloseFile();

			// Generate the central directory.
			$x = strlen($this->outdata);
			$x2 = $x;
			$centraldirstartpos = $this->outdatasize;
			$has64bit = false;
			foreach ($this->centraldirs as $dirinfo)
			{
				self::SetBytes($this->outdata, $x, "\x50\x4B\x01\x02", 4);
				self::SetUInt8($this->outdata, $x, (int)($dirinfo["made_by_version"] * 10));
				self::SetUInt8($this->outdata, $x, $dirinfo["made_by_os"]);
				self::SetUInt16($this->outdata, $x, (int)($dirinfo["version_required"] * 10));
				self::SetUInt16($this->outdata, $x, $dirinfo["flags"]);
				self::SetUInt16($this->outdata, $x, $dirinfo["compress_method"]);

				// Calculate the MS-DOS date/time.
				self::SetUInt16($this->outdata, $x, self::GetDOSTime($dirinfo["last_modified"]));
				self::SetUInt16($this->outdata, $x, self::GetDOSDate($dirinfo["last_modified"]));

				self::SetUInt32($this->outdata, $x, $dirinfo["crc32"]);

				if ($dirinfo["64bit"])
				{
					self::SetUInt32($this->outdata, $x, 0xFFFFFFFF);
					self::SetUInt32($this->outdata, $x, 0xFFFFFFFF);

					$has64bit = true;
				}
				else
				{
					self::SetUInt32($this->outdata, $x, $dirinfo["compressed_size"]);
					self::SetUInt32($this->outdata, $x, $dirinfo["uncompressed_size"]);
				}

				self::SetUInt16($this->outdata, $x, strlen($dirinfo["filename"]));

				$extrastr = self::GenerateExtraFieldsStr($dirinfo, true);
				self::SetUInt16($this->outdata, $x, strlen($extrastr));
				self::SetUInt16($this->outdata, $x, strlen($dirinfo["comment"]));

				self::SetUInt16($this->outdata, $x, ($dirinfo["64bit"] ? 0xFFFF : $dirinfo["disk_start_num"]));
				self::SetUInt16($this->outdata, $x, $dirinfo["internal_file_attrs"]);
				self::SetUInt32($this->outdata, $x, $dirinfo["external_file_attrs"]);
				self::SetUInt32($this->outdata, $x, ($dirinfo["64bit"] ? 0xFFFFFFFF : $dirinfo["header_offset"]));

				self::SetBytes($this->outdata, $x, $dirinfo["filename"], strlen($dirinfo["filename"]));
				self::SetBytes($this->outdata, $x, $extrastr, strlen($extrastr));
				self::SetBytes($this->outdata, $x, $dirinfo["comment"], strlen($dirinfo["comment"]));
			}

			$centraldirsize = $x - $x2;

			$this->outdatasize += $centraldirsize;
			$x2 = $x;

			// Generate the Zip64 End of Central Directory record and locator.
			if ($has64bit || $this->disknum >= 0xFFFF || count($this->centraldirs) >= 0xFFFF || ($centraldirsize < 0 || $centraldirsize > 0x7FFFFFFF) || ($centraldirstartpos < 0 || $centraldirstartpos > 0x7FFFFFFF))
			{
				// Zip64 End of Central Directory record.
				$zip64startpos = $this->outdatasize;
				self::SetBytes($this->outdata, $x, "\x50\x4B\x06\x06", 4);
				self::SetUInt64($this->outdata, $x, 44);
				self::SetUInt8($this->outdata, $x, 63);  // Version made by (6.3).
				self::SetUInt8($this->outdata, $x, 11);  // MVS (OS/390 - Z/OS).  Copied from a ZIP file I found with a MS-DOS "source".  IBM managed to really mess up this file format.
				self::SetUInt16($this->outdata, $x, 45);  // Version needed to extract (4.5).
				self::SetUInt32($this->outdata, $x, $this->disknum);
				self::SetUInt32($this->outdata, $x, $this->disknum);
				self::SetUInt64($this->outdata, $x, count($this->centraldirs));
				self::SetUInt64($this->outdata, $x, count($this->centraldirs));
				self::SetUInt64($this->outdata, $x, $centraldirsize);
				self::SetUInt64($this->outdata, $x, $centraldirstartpos);
				// No extensible data needed.  This isn't OS/390.

				// Zip64 End of Central Directory locator.
				self::SetBytes($this->outdata, $x, "\x50\x4B\x06\x07", 4);
				self::SetUInt32($this->outdata, $x, $this->disknum);
				self::SetUInt64($this->outdata, $x, $zip64startpos);
				self::SetUInt32($this->outdata, $x, $this->disknum + 1);

				$this->outdatasize += $x - $x2;
				$x2 = $x;
			}

			// Generate End of Central Directory record.
			self::SetBytes($this->outdata, $x, "\x50\x4B\x05\x06", 4);
			self::SetUInt16($this->outdata, $x, ($this->disknum >= 0xFFFF ? 0xFFFF : $this->disknum));
			self::SetUInt16($this->outdata, $x, ($this->disknum >= 0xFFFF ? 0xFFFF : $this->disknum));
			self::SetUInt16($this->outdata, $x, (count($this->centraldirs) >= 0xFFFF ? 0xFFFF : count($this->centraldirs)));
			self::SetUInt16($this->outdata, $x, (count($this->centraldirs) >= 0xFFFF ? 0xFFFF : count($this->centraldirs)));
			self::SetUInt32($this->outdata, $x, (($centraldirsize < 0 || $centraldirsize > 0x7FFFFFFF) ? 0xFFFFFFFF : $centraldirsize));
			self::SetUInt32($this->outdata, $x, (($centraldirstartpos < 0 || $centraldirstartpos > 0x7FFFFFFF) ? 0xFFFFFFFF : $centraldirstartpos));
			self::SetUInt16($this->outdata, $x, strlen($comment));
			self::SetBytes($this->outdata, $x, $comment, strlen($comment));

			$this->open = false;
			$this->centraldirs = array();

			return true;
		}

		public function BytesAvailable()
		{
			return strlen($this->outdata);
		}

		public function Read()
		{
			$result = $this->outdata;
			$this->outdata = "";

			return $result;
		}

		// In general, this function should be treated as internal.
		public static function AppendZip64ExtraField(&$extrafields, $origsize)
		{
			$extrafields[] = array(
				"header_id" => self::EXTRA_FIELD_ZIP64,
				"uncompressed_size" => $origsize,
				"compressed_size" => 0,
				"header_offset" => 0,
				"disk_start_num" => 0
			);
		}

		public static function AppendOS2ExtraField(&$extrafields, $os2extendedattrs)
		{
			$cancompress = DeflateStream::IsSupported();

			$extrafields[] = array(
				"header_id" => self::EXTRA_FIELD_OS2,
				"uncompressed_size" => strlen($os2extendedattrs),
				"compress_method" => ($cancompress ? self::COMPRESS_METHOD_DEFLATE : self::COMPRESS_METHOD_STORE),
				"crc32" => crc32($os2extendedattrs),
				"var" => ($cancompress ? DeflateStream::Compress($os2extendedattrs) : $os2extendedattrs)
			);
		}

		public static function AppendNTFSExtraField(&$extrafields, $lastmodified, $lastaccessed, $created)
		{
			// The number of seconds from Jan 1, 1601 to Jan 1, 1970.
			$filetimeepoch = 11644473600;

			// Windows FILETIME timestamp calculations are measured in 100 nanosecond increments from Jan 1, 1601.
			$extrafields[] = array(
				"header_id" => self::EXTRA_FIELD_NTFS,
				"tags" => array(
					array(
						"attribute" => self::EXTRA_FIELD_NTFS_TAG_TIMESTAMP,
						"mtime" => ($lastmodified + $filetimeepoch) * 10000000,
						"atime" => ($lastaccessed + $filetimeepoch) * 10000000,
						"ctime" => ($created + $filetimeepoch) * 10000000
					)
				)
			);
		}

		public static function AppendUNIXExtraField(&$extrafields, $lastaccessed, $lastmodified, $uid, $gid, $extradata = "")
		{
			$extrafields[] = array(
				"header_id" => self::EXTRA_FIELD_UNIX,
				"atime" => $lastaccessed,
				"mtime" => $lastmodified,
				"uid" => $uid,
				"gid" => $gid,
				"var" => $extradata
			);
		}

		// Generate extra fields string.
		protected static function GenerateExtraFieldsStr($dir, $centraldir)
		{
			$str = "";
			$x = 0;
			foreach ($dir["extra_fields"] as $extrafield)
			{
				if (is_string($extrafield))  self::SetBytes($str, $x, $extrafield, strlen($extrafield));
				else if ($extrafield["header_id"] === self::EXTRA_FIELD_ZIP64)
				{
					self::SetUInt16($str, $x, self::EXTRA_FIELD_ZIP64);
					self::SetUInt16($str, $x, ($centraldir ? 28 : 16));
					self::SetUInt64($str, $x, ($dir["flags"] & self::FLAG_USE_DATA_DESCRIPTOR ? 0 : $extrafield["uncompressed_size"]));
					self::SetUInt64($str, $x, ($dir["flags"] & self::FLAG_USE_DATA_DESCRIPTOR ? 0 : $extrafield["compressed_size"]));

					if ($centraldir)
					{
						self::SetUInt64($str, $x, $extrafield["header_offset"]);
						self::SetUInt32($str, $x, $extrafield["disk_start_num"]);
					}
				}
				else if ($extrafield["header_id"] === self::EXTRA_FIELD_OS2)
				{
					self::SetUInt16($str, $x, self::EXTRA_FIELD_OS2);
					self::SetUInt16($str, $x, 10 + strlen($extrafield["var"]));
					self::SetUInt32($str, $x, $extrafield["uncompressed_size"]);
					self::SetUInt16($str, $x, $extrafield["compress_method"]);
					self::SetUInt32($str, $x, $extrafield["crc32"]);
					self::SetBytes($str, $x, $extrafield["var"], strlen($extrafield["var"]));
				}
				else if ($extrafield["header_id"] === self::EXTRA_FIELD_NTFS)
				{
					self::SetUInt16($str, $x, self::EXTRA_FIELD_NTFS);

					// Calculate size.
					$y = 4;
					foreach ($extrafield["tags"] as $tag)
					{
						if ($tag["attribute"] === self::EXTRA_FIELD_NTFS_TAG_TIMESTAMP)  $y += 28;
					}

					self::SetUInt16($str, $x, $y);
					self::SetUInt32($str, $x, 0);  // Reserved.

					// Write tags.
					foreach ($extrafield["tags"] as $tag)
					{
						if ($tag["attribute"] === self::EXTRA_FIELD_NTFS_TAG_TIMESTAMP)
						{
							self::SetUInt16($str, $x, self::EXTRA_FIELD_NTFS_TAG_TIMESTAMP);
							self::SetUInt16($str, $x, 24);
							self::SetUInt64($str, $x, $tag["mtime"]);
							self::SetUInt64($str, $x, $tag["atime"]);
							self::SetUInt64($str, $x, $tag["ctime"]);
						}
					}
				}
				else if ($extrafield["header_id"] === self::EXTRA_FIELD_UNIX)
				{
					self::SetUInt16($str, $x, self::EXTRA_FIELD_UNIX);
					self::SetUInt16($str, $x, 12 + strlen($extrafield["var"]));
					self::SetUInt32($str, $x, $extrafield["atime"]);
					self::SetUInt32($str, $x, $extrafield["mtime"]);
					self::SetUInt16($str, $x, $extrafield["uid"]);
					self::SetUInt16($str, $x, $extrafield["gid"]);
					self::SetBytes($str, $x, $extrafield["var"], strlen($extrafield["var"]));
				}
			}

			return $str;
		}

		public static function MakeUnixExternalAttribute($mode, $unixtype = self::FILE_ATTRIBUTE_UNIX_DEVICE_REGULAR)
		{
			return ((($mode & 0xFFFF) << 16) | ($mode & 0xF000 ? 0 : $unixtype));
		}

		public static function InitCentralDirHeader($options = array(), $dostype = self::FILE_ATTRIBUTE_MSDOS_ARCHIVE)
		{
			$os = php_uname("s");
			$windows = (strtoupper(substr($os, 0, 3)) == "WIN");

			$defaults = array(
				"made_by_version" => 6.3,
				"made_by_os" => ($windows && !isset($options["unix_attrs"]) ? self::MADE_BY_MSDOS : self::MADE_BY_UNIX),
				"version_required" => 0,
				"flags" => 0,
				"compress_method" => self::COMPRESS_METHOD_STORE,
				"last_modified" => 0,
				"64bit" => false,
				"crc32" => 0,
				"compressed_size" => 0,
				"uncompressed_size" => 0,
				"bytes_left" => 0,
				"filename" => "",
				"extra_fields" => array(),
				"comment" => "",
				"disk_start_num" => 0,
				"internal_file_attrs" => 0,
				"external_file_attrs" => $dostype,
				"header_offset" => 0
			);

			if (!$windows || isset($options["unix_attrs"]))
			{
				if ($dostype & self::FILE_ATTRIBUTE_MSDOS_DIRECTORY)  $unixattrs = self::MakeUnixExternalAttribute((isset($options["unix_attrs"]) ? $options["unix_attrs"] : 0775), self::FILE_ATTRIBUTE_UNIX_DEVICE_DIRECTORY);
				else if ($dostype & self::FILE_ATTRIBUTE_MSDOS_SYMLINK)  $unixattrs = self::MakeUnixExternalAttribute((isset($options["unix_attrs"]) ? $options["unix_attrs"] : 0777), self::FILE_ATTRIBUTE_UNIX_DEVICE_SYMLINK);
				else  $unixattrs = self::MakeUnixExternalAttribute(isset($options["unix_attrs"]) ? $options["unix_attrs"] : 0664);

				$defaults["external_file_attrs"] |= $unixattrs;
			}

			return $options + $defaults;
		}

		protected function WriteLocalFileHeader()
		{
			$x = strlen($this->outdata);
			$x2 = $x;

			self::SetBytes($this->outdata, $x, "\x50\x4B\x03\x04", 4);
			self::SetUInt16($this->outdata, $x, (int)($this->currdir["version_required"] * 10));
			self::SetUInt16($this->outdata, $x, $this->currdir["flags"]);
			self::SetUInt16($this->outdata, $x, $this->currdir["compress_method"]);

			// Calculate the MS-DOS date/time.
			self::SetUInt16($this->outdata, $x, self::GetDOSTime($this->currdir["last_modified"]));
			self::SetUInt16($this->outdata, $x, self::GetDOSDate($this->currdir["last_modified"]));

			if ($this->currdir["flags"] & self::FLAG_USE_DATA_DESCRIPTOR)
			{
				self::SetUInt32($this->outdata, $x, 0);
				self::SetUInt32($this->outdata, $x, 0);
				self::SetUInt32($this->outdata, $x, 0);
			}
			else if ($this->currdir["64bit"])
			{
				self::SetUInt32($this->outdata, $x, $this->currdir["crc32"]);
				self::SetUInt32($this->outdata, $x, 0xFFFFFFFF);
				self::SetUInt32($this->outdata, $x, 0xFFFFFFFF);
			}
			else
			{
				self::SetUInt32($this->outdata, $x, $this->currdir["crc32"]);
				self::SetUInt32($this->outdata, $x, $this->currdir["compressed_size"]);
				self::SetUInt32($this->outdata, $x, $this->currdir["uncompressed_size"]);
			}

			self::SetUInt16($this->outdata, $x, strlen($this->currdir["filename"]));

			$extrastr = self::GenerateExtraFieldsStr($this->currdir, false);
			self::SetUInt16($this->outdata, $x, strlen($extrastr));

			self::SetBytes($this->outdata, $x, $this->currdir["filename"], strlen($this->currdir["filename"]));
			self::SetBytes($this->outdata, $x, $extrastr, strlen($extrastr));

			$this->outdatasize += $x - $x2;
		}

		protected function WriteDataDescriptor()
		{
			if (!($this->currdir["flags"] & self::FLAG_USE_DATA_DESCRIPTOR))  return;

			// Clear the flag.
			$this->currdir["flags"] ^= self::FLAG_USE_DATA_DESCRIPTOR;

			$x = strlen($this->outdata);
			$x2 = $x;

			self::SetBytes($this->outdata, $x, "\x50\x4B\x07\x08", 4);
			self::SetUInt32($this->outdata, $x, $this->currdir["crc32"]);

			if ($this->currdir["64bit"])
			{
				self::SetUInt64($this->outdata, $x, $this->currdir["compressed_size"]);
				self::SetUInt64($this->outdata, $x, $this->currdir["uncompressed_size"]);
			}
			else
			{
				self::SetUInt32($this->outdata, $x, $this->currdir["compressed_size"]);
				self::SetUInt32($this->outdata, $x, $this->currdir["uncompressed_size"]);
			}

			$this->outdatasize += $x - $x2;
		}

		// Oh dear.  Why.
		public static function GetDOSDate($ts)
		{
			// 7 bits year, 4 bits month, 5 bits day.
			return ((date("Y", $ts) - 1980) << 9) | (date("n", $ts) << 5) | date("j", $ts);
		}

		public static function GetDOSTime($ts)
		{
			// 5 bits hour, 6 bits minute, 5 bits seconds divided by 2.
			return (date("H", $ts) << 11) | (date("i", $ts) << 5) | (int)(date("s", $ts) / 2);
		}

		public static function SetUInt8(&$data, &$x, $val)
		{
			self::SetBytes($data, $x, chr($val), 1);
		}

		public static function SetUInt16(&$data, &$x, $val)
		{
			self::SetBytes($data, $x, pack("v", $val), 2);
		}

		public static function SetUInt32(&$data, &$x, $val)
		{
			self::SetBytes($data, $x, pack("V", $val), 4);
		}

		public static function SetUInt64(&$data, &$x, $val)
		{
			if (PHP_INT_SIZE >= 8)  self::SetBytes($data, $x, pack("P", $val), 8);
			else
			{
				$val2 = (int)($val % 0x10000);
				$val = ($val - $val2) / 0x10000;
				self::SetBytes($data, $x, pack("v", $val2), 2);

				$val2 = (int)($val % 0x10000);
				$val = ($val - $val2) / 0x10000;
				self::SetBytes($data, $x, pack("v", $val2), 2);

				$val2 = (int)($val % 0x10000);
				$val = ($val - $val2) / 0x10000;
				self::SetBytes($data, $x, pack("v", $val2), 2);

				$val2 = (int)($val % 0x10000);
				self::SetBytes($data, $x, pack("v", $val2), 2);

				return;
			}
		}

		public static function SetBytes(&$data, &$x, $val, $size)
		{
			for ($x2 = 0; $x2 < $size; $x2++)
			{
				$data[$x] = (isset($val[$x2]) ? $val[$x2] : "\x00");

				$x++;
			}
		}
	}
?>