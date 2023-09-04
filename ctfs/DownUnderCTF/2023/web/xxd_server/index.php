<?php

// Emulate the behavior of command line 'xxd' tool
function xxd(string $s): string {
	$out = '';
	$ctr = 0;
	foreach (str_split($s, 16) as $v) {
		$hex_string = implode(' ', str_split(bin2hex($v), 4));
		$ascii_string = '';
		foreach (str_split($v) as $c) {
			$ascii_string .= $c < ' ' || $c > '~' ? '.' : $c;
		}
		$out .= sprintf("%08x: %-40s %-16s\n", $ctr, $hex_string, $ascii_string);
		$ctr += 16;
	}
	return $out;
}

$message = '';

// Is there an upload?
if (isset($_FILES['file-upload'])) {
	$upload_dir = 'uploads/' . bin2hex(random_bytes(8));
	$upload_path = $upload_dir . '/' . basename($_FILES['file-upload']['name']);
	mkdir($upload_dir);
	$upload_contents = xxd(file_get_contents($_FILES['file-upload']['tmp_name']));
	if (file_put_contents($upload_path, $upload_contents)) {
		$message = 'Your file has been uploaded. Click <a href="' . htmlspecialchars($upload_path) . '">here</a> to view';
	} else {
	    $message = 'File upload failed.';
	}
}

?>
<!DOCTYPE html>
<html>
<head>
    <title>xxd-server</title>
        <style>
        body {
            background-color: #fff;
            color: #000;
            font-family: Arial, sans-serif;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            text-align: center;
            border: 2px solid #000;
            padding: 20px;
            border-radius: 10px;
        }

        h1 {
            color: #000;
        }

        #file-upload {
            display: none; /* hide the actual input */
        }

        /* Style the label to look like a button */
        label[for="file-upload"] {
            display: inline-block;
            background-color: #000;
            color: #fff;
            padding: 10px 20px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        label[for="file-upload"]:hover {
            background-color: #666;
        }

        #submit-button {
            margin-top: 20px;
            background-color: #000;
            color: #fff;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        #submit-button:hover {
            background-color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>xxd-server</h1>
        <p>Our patented hex technology&trade; allows you to view the binary data of any file. Try it here!</p>
        <form action="/" method="POST" enctype="multipart/form-data">
            <input type="file" id="file-upload" name="file-upload">
            <label for="file-upload">Select File</label>
            <br>
            <input type="submit" id="submit-button" value="Upload">
        </form>
        <?= $message ? '<p>' . $message . '</p>' : ''; ?>
    </div>
</body>
</html>



