<!DOCTYPE html>
<html>
<head>
    <style>
        body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f0f0f0;
}

.container {
    width: 80%;
    margin: auto;
    padding: 20px;
}

h1, h2 {
    text-align: center;
    color: #333;
}

form {
    background-color: #fff;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
}

input[type="text"], input[type="password"] {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
    border: 1px solid #ccc;
}

input[type="submit"] {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    width: 100%;
}
/* ?src=what? */

    </style>
</head>
<body>
    
    <div class="container">
        <h1>Howdy, Can you break in ? But as who ? </h1>
        <h2>Too many admins ?</h2>
        <form action="" method="post">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password">
            <input type="submit" value="Submit">
        </form>

        <?php
error_reporting(E_ALL & ~E_WARNING);
// The MySQL service named in the docker-compose.yml.
$host = 'db';
$srcParam = $_GET['src'];

if ($srcParam) {
    // The 'src' parameter is set, so highlight the source code
    highlight_file(__FILE__);
}
// Database user name
$user = getenv('MYSQL_USER');
$pass = getenv('MYSQL_ROOT_PASSWORD');
$database = getenv('MYSQL_DATABASE');





// Check the MySQL connection status
$conn = new mysqli($host, $user, $pass, $database);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} else {

    // Fetch the 'user' parameter from the query string
    $userParam = $_GET['user'];

    // Use prepared statement to prevent SQL injection
    if($userParam){
    if($userParam !=  "all"){
    $query = "SELECT username, password, bio FROM users where username = '$userParam' ";
    }else{
    $query = "SELECT username, password, bio FROM users ";

    }
    $result = $conn->query($query);
   
    // Display the result in a table
    echo "<table border='1'>";
    echo "<tr><th>S.no</th><th>Username</th><th>Password(MD5 hashes)</th></tr>";

    // Fetch and display the data
    $i = 0;
    while ($row = mysqli_fetch_row($result)) {
        echo "<tr><td>".$i."</td><td>" . $row[0] . "</td><td>" . $row[1] . "</td></tr>";
        $i++;
    }

    echo "</table>";
}
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $username = $_POST['username'];
        $password = $_POST['password'];
        
        if (empty($username) || empty($password)) {
            echo "Please fill in both fields.";
        } else {
    $query = "SELECT username, password, bio FROM users WHERE username = '$username' ";
    $result = $conn->query($query);
    $mysupersecurehash = md5(2*2*13*13*((int)$password));
    $i =0 ;
    while ($row = mysqli_fetch_row($result)) {
        if((int)$row[1] == $mysupersecurehash && $mysupersecurehash == 0e0776470569150041331763470558650263116470594705){
        echo "<h1>You win</h1> \n";
    echo "Did you really? \n";
        echo "<tr><td>" .$i. " </td><td> "  . $row[0] . " </td><td> " . $row[1] . " </td><td> " . $row[2] . " </td></tr>";
        $i++;
    }else{
        echo "<h1>Wrong password</h1>";
    }
}
        }
    }
    // Close the MySQL connection
    $conn->close();
}
        ?>
    </div>
</body>
</html>
