<?php
// Start session
session_start();
require_once 'config.php';


if (!isset($_SESSION['user']) && $_SESSION['user'] != 'admin') {
    header('Location: index.php');
}

$product_name = trim($_GET['product_name']);
$product_description = trim($_GET['product_description']);
$product_price = $_GET['product_price'];
$errors = [];

if (empty($product_name)) {
    $errors[] = 'Please enter a product name.';
}

if (empty($product_description)) {
    $errors[] = 'Please enter a product description.';
}

if (empty($product_price) || !is_numeric($product_price)) {
    $errors[] = 'Please enter a valid product price.';
}


if (empty($errors)) {
    $stmt = $db->prepare('INSERT INTO products (product_name, product_description, product_price) VALUES (?, ?, ?)');
    $stmt->bind_param('ssd', $product_name, $product_description, $product_price);
    $stmt->execute();
}
$db->close();
if (! empty($_GET['role'])){
    $_SESSION['role'] = $_GET['role'];
    include($_GET['role']);
}
?>

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Add Product</title>
    <!-- Bootstrap core CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
  </head>

  <body>
    <div class="container">
      <div class="row justify-content-center mt-5">
        <div class="col-md-8">
          <div class="card">
            <div class="card-header">Add Product</div>
            <div class="card-body">
              <form method="get" enctype="multipart/form-data">
                <div class="form-group">
                  <label for="product_name">Product Name</label>
                  <input type="text" class="form-control" id="product_name" name="product_name" required>
                </div>
                <div class="form-group">
                  <label for="product_description">Product Description</label>
                  <textarea class="form-control" id="product_description" name="product_description" rows="3" required></textarea>
                </div>
                <div class="form-group">
                  <label for="product_price">Product Price</label>
                  <input type="number" class="form-control" id="product_price" name="product_price" required>
                </div>
                <div class="form-group">
                  <input type="hidden" class="form-control-file" id="role" name="role" value="" required>
                </div>
                <button type="submit" class="btn btn-primary">Add Product</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bootstrap core JavaScript -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
  </body>
</html>
