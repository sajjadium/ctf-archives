<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Website Title</title>
  <link rel="stylesheet" href="css/styles.css">
</head>

<body>
  <nav class="navbar">
    <div class="container">
      <div class="logo">
          <img src="images/sky.png" alt="Your Logo">
      </div>
      <ul class="menu">
        <li><a href="#" onclick="toggleContent('home')">Home</a></li>
	<li><a href="#chat" onclick="toggleChat()">Chat</a></li>
	<li><a href="#" onclick="toggleContent('gallery')">Gallery</a></li>
      </ul>
    </div>
  </nav>

  <div class="content" id='home'>
    <h1>Welcome to Detroit</h1>
    <p>If you already own a Ford, feel free to share your passion here with other fans. Perhaps you can share more than just your passion.</p>
  </div>

  <div id="gallery" class="content">
    <h1>Gallery</h1>
    <div id="gallery-images">
      <img src="images/pic1.jpg" alt="Image 1">
      <img src="images/pic2.jpg" alt="Image 2">
      <img src="images/pic3.jpg" alt="Image 3">
    </div>

   <button onclick="toggleUploadForm()">Upload Image</button>

    <div id="gallery-upload-form" style="display: none">
      <h2>Upload an Image!</h2>
      <form action="" method="POST" enctype="multipart/form-data">
        <label for="fileToUpload">Select a file:</label>
        <input type="file" name="fileToUpload" id="fileToUpload">
        <input type="submit" value="Upload" name="submit">
      </form>
    </div>
  </div>
  <div id="chat-box" style="display: none">
    <h1>Share your passion here! To close the chat, click on "chat" again.</h1>
    <div id="chat-messages"></div>
    <input type="text" id="chat-input" placeholder="Type your message">
    <button id="send-button">Send</button>
  </div>
  <script src="js/script.js" ></script>
    <?php error_reporting(0) ?>
    <?php
    $files = $_FILES["fileToUpload"];
    $uploadOk = true;
    if($files["name"] != ""){
      $target_dir = urldecode("images/" . $files["name"]);
      if(strpos($target_dir,"..") !== false){
        $uploadOk = false;
      }
      if(filesize($files["tmp_name"]) > 1*1000){
        $uploadOk = false;
        echo "too big!!!";
      }
      $extension = strtolower(pathinfo($target_dir,PATHINFO_EXTENSION));
      $finfo = finfo_open(FILEINFO_MIME_TYPE);
      $type = finfo_file($finfo,$files["tmp_name"]);
      finfo_close($finfo);
      if($extension != "gif" || strpos($type,"image/gif") === false){
        echo " Sorry, only gif files are accepted";
        $uploadOk = false;
      }
      $target_dir = strtok($target_dir,chr(0));
      if($uploadOk && move_uploaded_file($files["tmp_name"],$target_dir)){
        echo "<a href='$target_dir'>uploaded gif here go see it!</a>";
      }
    }

  ?>
</body>

</html>
