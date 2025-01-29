<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>PNG to ICO</title>
  <style type="text/css">
    html, body {
      background: #F9F9F9;
      margin: 0;
      font-family: system-ui, sans-serif;
      color: #444;
      text-align: center;
      min-height: 100vh;
    }
    h1 {
      margin: 0;
      display: block;
      width: calc(100% - 8px);
      background: linear-gradient(to right, #111, #222);
      color: #FFF;
      padding: 4px;
      user-select: none;
      cursor: pointer;
    }
    a {
      color: #b53836;
      text-decoration: none;
    }
    #header {
      background: linear-gradient(to right, #222, #444);
      color: #FFF;
      margin: 0;
    }
    #footer {
      width: 100%;
      color: #aaa;
      margin: 0;
    }
    #info {
      display: flex;
      align-items: center;
      text-align: left;
      padding: 32px;
      gap: 32px;
      max-width: 640px;
      margin: auto;
    }
    .format {
      border: 1px solid #5A5A5A;
      border-radius: 4px;
      padding: 8px 16px;
      user-select: none;
      cursor: pointer;
    }
    .btn {
      background: #B53836;
      color: #FFF;
      border-radius: 4px;
      display: inline-block;
      margin: 8px;
      padding: 16px 32px;
      font-size: 24px;
      user-select: none;
      cursor: pointer;
      transition: 0.1s filter;
      filter: brightness(1.0);
      &:hover {
        filter: brightness(1.1);
      }
      &:active {
        filter: brightness(0.9);
      }
    }
    #uploadBtn {
     background: #d30069; 
    }
    input:invalid ~ #uploadBtn {
      display: none;
    }
    input:valid ~ #fileBtn {
      display: none;
    }
    #modal {
      display: flex;
      align-items: center;
      justify-content: center;
      position: fixed;
      top: 0;
      left: 0;
      background: #0007;
      width: 100%;
      height: 100%;
      &> div {
        width: 600px;
        height: fit-content;
        border-radius: 4px;
        background: #FFF;
        margin-bottom: 20%;
        transition: 0.75s opacity, 0.75s scale;
        opacity: 1;
        scale: 1;
        @starting-style {
          opacity: 0;
          scale: 0.75;
        }
      }
      opacity: 1;
      transition: 0.75s background, 0.75s opacity;
      @starting-style {
        background: #0000;
      }
      &:has(#close:checked) {
        opacity: 0;
        user-select: none;
        pointer-events: none;
      }
    }
    #icon {
      box-shadow: 1px 1px 13px 0 #d300df;
      width: 64px;
      height: 64px;
      transition: 2s opacity, 2s filter;
      opacity: 1;
      filter: blur(0px);
      @starting-style {
        opacity: 0;
        filter: blur(32px);
      }
    }
    #why {
      display: grid;
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      text-align: left;
      padding: 32px;
      gap: 32px;
      max-width: 800px;
      margin: auto;
    }
  </style>
</head>
<body>
<div id="header">
  <h1>KittyConvert</h1>
  <div id="info">
    <div>
      <h2>PNG to ICO Converter</h2>
      <p>KittyConvert converts your image files online. Amongst no others, we support PNG. You can not use the options to control image resolution, quality and file size.</p>
    </div>
    <div>
      <p style="white-space: nowrap; font-size: 18px;">convert <span class="format">PNG</span> to <span class="format">ICO</span></p>
    </div>
  </div>
</div>
<?php
// Disable annoying warnings
error_reporting(E_ERROR | E_PARSE);
$success = false;

if (isset($_FILES['file'])) {
  $base_dir = "/var/www/html/";
  $ico_file = "uploads/" . preg_replace("/^(.+)\\..+$/", "$1.ico", basename($_FILES["file"]["name"]));
  
  if ($_FILES["file"]["size"] > 8000) {
    echo "<p>Sorry, your file is too large you need to buy Nitro.</p>";
  } else {
    require( dirname( __FILE__ ) . '/class-php-ico.php' );
    $ico_lib = new PHP_ICO( $_FILES["file"]["tmp_name"], array( array( 32, 32 ), array( 64, 64 ) ) );
    $ico_lib->save_ico( $base_dir . $ico_file );
    $success = true;
  }
}
?>
<form action="/" method="post" enctype="multipart/form-data">
  <input type="file" name="file" id="file" accept=".png" required style="display:none"><br>
  <label class="btn" for="file" id="fileBtn">Select File</label>
  <input type="submit" value="Convert" name="submit" class="btn" id="uploadBtn">
</form>
<h2>Why use KittyConvert?</h2>
<div id="why">
  <div>
    <h2>2 Formats Supported</h2>
    <p>Ngl KittyConvert is kinda mid for file conversions. We support no audio, video, document, ebook, archive, spreadsheet, and presentation formats. But the upside of that is that you don't need to download complicated and expensive software such as ImageMagick or Adobe Photoshop just to convert your files.</p>
  </div>
  <div>
    <h2>Business Model</h2>
    <p>KittyConvert does not make money by selling your data, we tried it but we didn't make much money. So instead we have come up with an alternative business model to bring in funding. Read more about that in our <a href="https://en.wikipedia.org/wiki/Cat_caf%C3%A9">Business Model</a>.</p>
  </div>
  <div>
    <h2>Medium-Quality Conversions</h2>
    <p>Besides using open source software under the hood, we've tried to partner with various software vendors although nothing has come of it so far. Most conversion types can not be adjusted to your needs because it's easier to implement this way.</p>
  </div>
  <div>
    <h2>Powerful API</h2>
    <p>Our API allows custom integrations with your app. We don't like actually have an API but you can just see how the webapp works and curl the same endpoints so it's like having an API but epic.</p>
  </div>
</div>
<div id="footer">
© 2025 meow meow
<br><br>
</div>
<div id="modal" <?php if (!$success) echo 'style="display:none"'; ?>>
  <input type="checkbox" id="close" name="close" style="display:none">
  <div>
    <label for="close" style="font-size:16px; position:absolute; right: 8px; cursor: pointer;">x</label>
    <h2>You just made something awesome happen!</h2>
    <p>Here's your pawsome little ico file:</p>
    <?php if ($success) {
      echo '<a href="' . htmlspecialchars($ico_file) . '" download><img id="icon" src="' . htmlspecialchars($ico_file) . '" /></a>';
    } ?>
    <p>Click on it to download!</p>
  </div>
</div>
</body>
</html>