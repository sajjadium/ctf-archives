<?php
	// CRC32 stream class.
	// (C) 2020 CubicleSoft.  All Rights Reserved.
	//
	// Direct port from the CubicleSoft C++ implementation.

	class CRC32Stream
	{
		private $open, $hash, $crctable, $datareflect, $crcreflect, $firstcrc, $currcrc, $finalxor;
		private static $revlookup = array(0, 128, 64, 192, 32, 160, 96, 224, 16, 144, 80, 208, 48, 176, 112, 240, 8, 136, 72, 200, 40, 168, 104, 232, 24, 152, 88, 216, 56, 184, 120, 248, 4, 132, 68, 196, 36, 164, 100, 228, 20, 148, 84, 212, 52, 180, 116, 244, 12, 140, 76, 204, 44, 172, 108, 236, 28, 156, 92, 220, 60, 188, 124, 252, 2, 130, 66, 194, 34, 162, 98, 226, 18, 146, 82, 210, 50, 178, 114, 242, 10, 138, 74, 202, 42, 170, 106, 234, 26, 154, 90, 218, 58, 186, 122, 250, 6, 134, 70, 198, 38, 166, 102, 230, 22, 150, 86, 214, 54, 182, 118, 246, 14, 142, 78, 206, 46, 174, 110, 238, 30, 158, 94, 222, 62, 190, 126, 254, 1, 129, 65, 193, 33, 161, 97, 225, 17, 145, 81, 209, 49, 177, 113, 241, 9, 137, 73, 201, 41, 169, 105, 233, 25, 153, 89, 217, 57, 185, 121, 249, 5, 133, 69, 197, 37, 165, 101, 229, 21, 149, 85, 213, 53, 181, 117, 245, 13, 141, 77, 205, 45, 173, 109, 237, 29, 157, 93, 221, 61, 189, 125, 253, 3, 131, 67, 195, 35, 163, 99, 227, 19, 147, 83, 211, 51, 179, 115, 243, 11, 139, 75, 203, 43, 171, 107, 235, 27, 155, 91, 219, 59, 187, 123, 251, 7, 135, 71, 199, 39, 167, 103, 231, 23, 151, 87, 215, 55, 183, 119, 247, 15, 143, 79, 207, 47, 175, 111, 239, 31, 159, 95, 223, 63, 191, 127, 255);

		// PKZip, gzip, AUTODIN II, Ethernet, and FDDI.
		public static $default = array("poly" => 0x04C11DB7, "start" => 0xFFFFFFFF, "xor" => 0xFFFFFFFF, "refdata" => 1, "refcrc" => 1);

		public function __construct()
		{
			$this->open = false;
		}

		public function Init($options = false)
		{
			if ($options === false && function_exists("hash_init"))  $this->hash = hash_init("crc32b");
			else
			{
				if ($options === false)  $options = self::$default;

				$this->hash = false;
				$this->crctable = array();
				$poly = $this->LIM32($options["poly"]);
				for ($x = 0; $x < 256; $x++)
				{
					$c = $this->SHL32($x, 24);
					for ($y = 0; $y < 8; $y++)  $c = $this->SHL32($c, 1) ^ ($c & 0x80000000 ? $poly : 0);
					$this->crctable[$x] = $c;
				}

				$this->datareflect = $options["refdata"];
				$this->crcreflect = $options["refcrc"];
				$this->firstcrc = $options["start"];
				$this->currcrc = $options["start"];
				$this->finalxor = $options["xor"];
			}

			$this->open = true;
		}

		public function AddData($data)
		{
			if (!$this->open)  return false;

			if ($this->hash !== false)  hash_update($this->hash, $data);
			else
			{
				$y = strlen($data);

				for ($x = 0; $x < $y; $x++)
				{
					if ($this->datareflect)  $this->currcrc = $this->SHL32($this->currcrc, 8) ^ $this->crctable[$this->SHR32($this->currcrc, 24) ^ self::$revlookup[ord($data[$x])]];
					else  $this->currcrc = $this->SHL32($this->currcrc, 8) ^ $this->crctable[$this->SHR32($this->currcrc, 24) ^ ord($data[$x])];
				}
			}

			return true;
		}

		public function Finalize()
		{
			if (!$this->open)  return false;

			if ($this->hash !== false)
			{
				$result = hexdec(hash_final($this->hash));

				$this->hash = hash_init("crc32b");
			}
			else
			{
				if ($this->crcreflect)
				{
					$tempcrc = $this->currcrc;
					$this->currcrc = self::$revlookup[$this->SHR32($tempcrc, 24)] | $this->SHL32(self::$revlookup[$this->SHR32($tempcrc, 16) & 0xFF], 8) | $this->SHL32(self::$revlookup[$this->SHR32($tempcrc, 8) & 0xFF], 16) | $this->SHL32(self::$revlookup[$this->LIM32($tempcrc & 0xFF)], 24);
				}
				$result = $this->currcrc ^ $this->finalxor;

				$this->currcrc = $this->firstcrc;
			}

			return $result;
		}

		// These functions are a hacky, but effective way of enforcing unsigned 32-bit integers onto a generic signed int.
		// Allow bitwise operations to work across platforms.  Minimum integer size must be 32-bit.
		private function SHR32($num, $bits)
		{
			$num = (int)$num;
			if ($bits < 0)  $bits = 0;

			if ($num < 0 && $bits)
			{
				$num = ($num >> 1) & 0x7FFFFFFF;
				$bits--;
			}

			return $this->LIM32($num >> $bits);
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
	}
?>