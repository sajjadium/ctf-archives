<?php
	// Deflate stream class.  Default is RFC1951 (raw deflate).  Supports RFC1950 (ZLIB) and RFC1952 (gzip).
	// (C) 2020 CubicleSoft.  All Rights Reserved.

	class DeflateStream
	{
		private $open, $fp, $filter, $compress, $indata, $outdata, $options;
		private static $supported;

		public function __construct()
		{
			$this->open = false;
		}

		public function __destruct()
		{
			$this->Finalize();
		}

		public static function IsSupported()
		{
			if (!is_bool(self::$supported))
			{
				self::$supported = function_exists("stream_filter_append") && function_exists("stream_filter_remove") && function_exists("gzcompress");
				if (self::$supported)
				{
					$data = self::Compress("test");
					if ($data === false || $data === "")  self::$supported = false;
					else
					{
						$data = self::Uncompress($data);
						if ($data === false || $data !== "test")  self::$supported = false;
					}
				}
			}

			return self::$supported;
		}

		public static function Compress($data, $compresslevel = -1, $options = array())
		{
			$ds = new DeflateStream;
			if (!$ds->Init("wb", $compresslevel, $options))  return false;
			if (!$ds->Write($data))  return false;
			if (!$ds->Finalize())  return false;
			$data = $ds->Read();

			return $data;
		}

		public static function Uncompress($data, $options = array("type" => "auto"))
		{
			$ds = new DeflateStream;
			if (!$ds->Init("rb", -1, $options))  return false;
			if (!$ds->Write($data))  return false;
			if (!$ds->Finalize())  return false;
			$data = $ds->Read();

			return $data;
		}

		public function Init($mode, $compresslevel = -1, $options = array())
		{
			if ($mode !== "rb" && $mode !== "wb")  return false;
			if ($this->open)  $this->Finalize();

			$this->fp = fopen("php://memory", "w+b");
			if ($this->fp === false)  return false;
			$this->compress = ($mode == "wb");
			if (!isset($options["type"]))  $options["type"] = "rfc1951";

			if ($options["type"] == "rfc1950")  $options["type"] = "zlib";
			else if ($options["type"] == "rfc1952")  $options["type"] = "gzip";

			if ($options["type"] != "zlib" && $options["type"] != "gzip" && ($this->compress || $options["type"] != "auto"))  $options["type"] = "raw";
			$this->options = $options;

			// Add the deflate filter.
			if ($this->compress)  $this->filter = stream_filter_append($this->fp, "zlib.deflate", STREAM_FILTER_WRITE, $compresslevel);
			else  $this->filter = stream_filter_append($this->fp, "zlib.inflate", STREAM_FILTER_READ);

			$this->open = true;
			$this->indata = "";
			$this->outdata = "";

			if ($this->compress)
			{
				if ($this->options["type"] == "zlib")
				{
					$this->outdata .= "\x78\x9C";
					$this->options["a"] = 1;
					$this->options["b"] = 0;
				}
				else if ($this->options["type"] == "gzip")
				{
					if (!class_exists("CRC32Stream", false))  require_once str_replace("\\", "/", dirname(__FILE__)) . "/crc32_stream.php";

					$this->options["crc32"] = new CRC32Stream();
					$this->options["crc32"]->Init();
					$this->options["bytes"] = 0;

					$this->outdata .= "\x1F\x8B\x08";
					$flags = 0;
					if (isset($this->options["filename"]))  $flags |= 0x08;
					if (isset($this->options["comment"]))  $flags |= 0x10;
					$this->outdata .= chr($flags);
					$this->outdata .= "\x00\x00\x00\x00";
					$this->outdata .= "\x00";
					$this->outdata .= "\x03";

					if (isset($this->options["filename"]))  $this->outdata .= str_replace("\x00", " ", $this->options["filename"]) . "\x00";
					if (isset($this->options["comment"]))  $this->outdata .= str_replace("\x00", " ", $this->options["comment"]) . "\x00";
				}
			}
			else
			{
				$this->options["header"] = false;
			}

			return true;
		}

		public function Read()
		{
			$result = $this->outdata;
			$this->outdata = "";

			return $result;
		}

		public function Write($data)
		{
			if (!$this->open)  return false;

			if ($this->compress)
			{
				if ($this->options["type"] == "zlib")
				{
					// Adler-32.
					$y = strlen($data);
					for ($x = 0; $x < $y; $x++)
					{
						$this->options["a"] = ($this->options["a"] + ord($data[$x])) % 65521;
						$this->options["b"] = ($this->options["b"] + $this->options["a"]) % 65521;
					}
				}
				else if ($this->options["type"] == "gzip")
				{
					$this->options["crc32"]->AddData($data);
					$this->options["bytes"] = $this->ADD32($this->options["bytes"], strlen($data));
				}

				$this->indata .= $data;
				while (strlen($this->indata) >= 65536)
				{
					fwrite($this->fp, substr($this->indata, 0, 65536));
					$this->indata = substr($this->indata, 65536);

					$this->ProcessOutput();
				}
			}
			else
			{
				$this->indata .= $data;
				$this->ProcessInput();
			}

			return true;
		}

		// Finalizes the stream.
		public function Finalize()
		{
			if (!$this->open)  return false;

			if (!$this->compress)  $this->ProcessInput(true);

			if (strlen($this->indata) > 0)
			{
				fwrite($this->fp, $this->indata);
				$this->indata = "";
			}

			// Removing the filter pushes the last buffer into the stream.
			stream_filter_remove($this->filter);
			$this->filter = false;

			$this->ProcessOutput();

			fclose($this->fp);

			if ($this->compress)
			{
				if ($this->options["type"] == "zlib")  $this->outdata .= pack("N", $this->SHL32($this->options["b"], 16) | $this->options["a"]);
				else if ($this->options["type"] == "gzip")  $this->outdata .= pack("V", $this->options["crc32"]->Finalize()) . pack("V", $this->options["bytes"]);
			}

			$this->open = false;

			return true;
		}

		private function ProcessOutput()
		{
			rewind($this->fp);

			// Hack!  Because ftell() on a stream with a filter is still broken even under the latest PHP a mere 11 years later.
			// See:  https://bugs.php.net/bug.php?id=49874
			ob_start();
			fpassthru($this->fp);
			$this->outdata .= ob_get_contents();
			ob_end_clean();

			rewind($this->fp);
			ftruncate($this->fp, 0);
		}

		private function ProcessInput($final = false)
		{
			// Automatically determine the type of data based on the header signature.
			if ($this->options["type"] == "auto")
			{
				if (strlen($this->indata) >= 3)
				{
					$zlibtest = unpack("n", substr($this->indata, 0, 2));

					if (substr($this->indata, 0, 3) === "\x1F\x8B\x08")  $this->options["type"] = "gzip";
					else if ((ord($this->indata[0]) & 0x0F) == 8 && ((ord($this->indata[0]) & 0xF0) >> 4) < 8 && $zlibtest[1] % 31 == 0)  $this->options["type"] = "zlib";
					else  $this->options["type"] = "raw";
				}
				else if ($final)  $this->options["type"] = "raw";
			}

			if ($this->options["type"] == "gzip")
			{
				if (!$this->options["header"])
				{
					if (strlen($this->indata) >= 10)
					{
						$idcm = substr($this->indata, 0, 3);
						$flg = ord($this->indata[3]);

						if ($idcm !== "\x1F\x8B\x08")  $this->options["type"] = "ignore";
						else
						{
							// Calculate the number of bytes to skip.  If flags are set, the size can be dynamic.
							$size = 10;
							$y = strlen($this->indata);

							// FLG.FEXTRA
							if ($size && ($flg & 0x04))
							{
								if ($size + 2 >= $y)  $size = 0;
								else
								{
									$xlen = unpack("v", substr($this->indata, $size, 2));
									$size = ($size + 2 + $xlen <= $y ? $size + 2 + $xlen : 0);
								}
							}

							// FLG.FNAME
							if ($size && ($flg & 0x08))
							{
								$pos = strpos($this->indata, "\x00", $size);
								$size = ($pos !== false ? $pos + 1 : 0);
							}

							// FLG.FCOMMENT
							if ($size && ($flg & 0x10))
							{
								$pos = strpos($this->indata, "\x00", $size);
								$size = ($pos !== false ? $pos + 1 : 0);
							}

							// FLG.FHCRC
							if ($size && ($flg & 0x02))  $size = ($size + 2 <= $y ? $size + 2 : 0);

							if ($size)
							{
								$this->indata = substr($this->indata, $size);
								$this->options["header"] = true;
							}
						}
					}
				}

				if ($this->options["header"] && strlen($this->indata) > 8)
				{
					fwrite($this->fp, substr($this->indata, 0, -8));
					$this->indata = substr($this->indata, -8);

					$this->ProcessOutput();
				}

				if ($final)  $this->indata = "";
			}
			else if ($this->options["type"] == "zlib")
			{
				if (!$this->options["header"])
				{
					if (strlen($this->indata) >= 2)
					{
						$cmf = ord($this->indata[0]);
						$flg = ord($this->indata[1]);
						$cm = $cmf & 0x0F;
						$cinfo = ($cmf & 0xF0) >> 4;

						// Compression method 'deflate' ($cm = 8), window size - 8 ($cinfo < 8), no preset dictionaries ($flg bit 5), checksum validates.
						if ($cm != 8 || $cinfo > 7 || ($flg & 0x20) || (($cmf << 8 | $flg) % 31) != 0)  $this->options["type"] = "ignore";
						else
						{
							$this->indata = substr($this->indata, 2);
							$this->options["header"] = true;
						}
					}
				}

				if ($this->options["header"] && strlen($this->indata) > 4)
				{
					fwrite($this->fp, substr($this->indata, 0, -4));
					$this->indata = substr($this->indata, -4);

					$this->ProcessOutput();
				}

				if ($final)  $this->indata = "";
			}

			if ($this->options["type"] == "raw")
			{
				fwrite($this->fp, $this->indata);
				$this->indata = "";

				$this->ProcessOutput();
			}

			// Only set when an unrecoverable header error has occurred for gzip or zlib.
			if ($this->options["type"] == "ignore")  $this->indata = "";
		}

		private function SHL32($num, $bits)
		{
			if ($bits < 0)  $bits = 0;

			return $this->LIM32((int)$num << $bits);
		}

		private function LIM32($num)
		{
			return (int)((int)$num & 0xFFFFFFFF);
		}

		private function ADD32($num, $num2)
		{
			$num = (int)$num;
			$num2 = (int)$num2;
			$add = ((($num >> 30) & 0x03) + (($num2 >> 30) & 0x03));
			$num = ((int)($num & 0x3FFFFFFF) + (int)($num2 & 0x3FFFFFFF));
			if ($num & 0x40000000)  $add++;
			$num = (int)(($num & 0x3FFFFFFF) | (($add & 0x03) << 30));

			return $num;
		}
	}
?>