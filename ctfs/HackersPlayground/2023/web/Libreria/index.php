<?php
include "./config.php";
$rows = 0;
$succ = -1;

if(isset($_GET['searchkey'])) {
	$succ = 0;

	$db = dbconnect();
    pg_prepare($db, "search_books", "SELECT * FROM books WHERE title ILIKE $1 LIMIT 100");
    $result = pg_execute($db, "search_books", array("%".$_GET['searchkey']."%"));
	pg_close($db);
	if($result) {
        $rows = pg_num_rows($result);
	}
}

?>

<!DOCTYPE html>
<!-- Site theme is from bookfinder(https://www.bookfinder.com) -->
<html class="no-js" lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Libreria</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
    <link href="style.css" rel="stylesheet" />
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-Fy6S3B9q64WdZWQUiU+q4/2Lc9npb8tCaSX9FK7E8HnRr0Jz8D6OP9dO5Vg3Q9ct" crossorigin="anonymous"></script>
  </head>
  <body>
    <script>
    // Function to do an Ajax call
    const showBookInfo = async (isbn) => {
      $("body").css("cursor", "progress");
      const response = await fetch('/rest.php?cmd=findbyisbn&isbn=' + isbn); // Generate the Response object
      $("body").css("cursor", "default");
      if (response.ok) {
        const jsonValue = await response.json(); // Get JSON value from the response body
        if (jsonValue.author == null) jsonValue.author = "(N/A)";
        tableData = '<table>'
                    + '<tr><td width="30%" style="padding:5px">Cover</td><td width="70%" style="padding:5px"><image src="' + jsonValue.image + '" width="150px" /></td></tr>'
                    + '<tr><td style="padding:5px">Title</td><td style="padding:5px">' + jsonValue.title + '</td></tr>'
                    + '<tr><td style="padding:5px">Author</td><td style="padding:5px">' + jsonValue.author + '</td></tr>'
                    + '<tr><td style="padding:5px">Price(KRW)</td><td style="padding:5px">' + jsonValue.price + '</td></tr>'
                    + '<tr><td style="padding:5px">Publisher</td><td style="padding:5px">' + jsonValue.publisher + '</td></tr>'
                    + '<tr><td style="padding:5px">Pub Date(YYYYMMDD)</td><td style="padding:5px">' + jsonValue.pubdate + '</td></tr>'
                    + '<tr><td style="padding:5px">ISBN</td><td style="padding:5px">' + jsonValue.isbn + '</td></tr>'
                    + '<tr><td style="padding:5px">Description</td><td style="padding:5px">' + jsonValue.description + '</td></tr>'
                    + '</table>'
        $('#sendreqbtn').remove();
        $('#modalLabel').text("Detailed Book Info");
        $('#modalbody').html(tableData);
        $('#exampleModal').modal('show');
      }
    };

    const requestBook = async () => {
        $("body").css("cursor", "progress");
        const isbn = $('#isbn').val();
        const response = await fetch('/rest.php?cmd=requestbook&isbn=' + isbn);
        $("body").css("cursor", "default");
        if (response.ok) {
            const jsonValue = await response.json();
            $('#modalbody').html(jsonValue.res);
            $('#sendreqbtn').remove();
        }
    };

    function askBuyBooks() {
        formdata = 'Please ask the staff nearby to buy the book.'
                    + '<form>'
                    + '<input id="isbn" type="text" name="isbn" placeholder="ISBN for the book" />'
                    + '</form>'
        $('#modalLabel').text("Ask yo buy a book.");
        $('#modalbody').html(formdata);
        $('#sendreqbtn').remove();
        $('#modalfooter').append('<button type="button" class="btn btn-primary name="sendreqbtn" id="sendreqbtn" onclick="requestBook()">Send Request</button>');
        $('#exampleModal').modal('show');
    }
    </script>
   <!-- Modal -->
    <div class="modal" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="modalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document" style="max-width: 800px;max-height:500px">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" name="modalLabel" id="modalLabel"></h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body" name="modalbody" id="modalbody"></div>
          <div class="modal-footer" name="modalfooter" id="modalfooter">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>

    <div id="page-top" class="bf-page-wrapper">
      <div class="bf-header-wrapper">
        <header class="bf-header">
          <div class="container-fluid">
            <div class="bf-main-nav">
              <div class="hidden-xs bf-language-switcher">
                <form class="">
                  <label class="">Language</label>
                  <select class="form-control interface-lang-select">
                    <option value="en" selected="">English</option>
                  </select>
                  </form>
              </div>
            </div>
          </div>
          <div class="container-fluid">
            <div class="bf-homelink ">
              <a href="#" class="">BookFinder.com</a>
            </div>
            <div class="bf-tagline">Find books for hakers</div>
          </div>
        </header><!-- /.bf-header -->
      </div>
      
    <!-- no quick search bar for the home page -->
    
      <div class="bf-content-wrapper">
        
    <div class="bf-content bf-home">
      <div class="bf-content-inner">
        <div class="container-fluid">
          <div class="row">
            <div class="col-md-102 col-sm-12 bf-home-search-form-col">
              <div class="bf-home-search-form bf-form">
                <h2>
                  Search books online
                </h2>
                    <!-- SEARCH FORM START -->
                    <form>
                      <div class="form-group">
                        <div class="row">
                          <label class="col-sm-3 col-xs-12 col-md-3 control-label" id="key_label">Keyword</label>
                          <div class="col-md-8 col-sm-8 col-xs-12">
                            <input autofocus="" class="form-control" id="search" name="searchkey" type="text" value="">
                          </div>
                        </div>
                      </div>
                      <div class="form-group">
                        <div class="row">
                          <label class="col-sm-3 col-xs-12 col-md-3 control-label" id="currency">Currency</label>
                          <div class="col-sm-6 col-xs-12">
                            <select class="form-control" id="bfs_currency" name="currency"><option value="krw">KRW(Korean WON)</option></select>
                          </div>
                        </div>
                      </div>                      <div class="form-group bf-home-search-form-submit">
                        <div class="row">
                          <div class="col-sm-offset-3 col-md-offset-3 col-sm-9 col-xs-12">
                            <button type="submit" class="btn btn-power modalButton">SEARCH</button>
                          </div>
                        </div>
                      </div>
                      <hr>
                    </form>
                    <!-- SEARCH FORM END -->
                  </div>

                </div>
              </div>

<?
    if ($rows > 0) {
?>
    <!-- show search result -->
    <div class="bf-home-search-form txt-center">

    <h2>Search Result</h2>
    <table>
        <thead>
            <tr>
                <th class="pin" width="10%">#</th>
                <th width="40%">Title</th>
                <th width="25%">Author</th>
                <th width="20%">ISBN</th>
                <th width="10%">Price(KRW)</th>
            </tr>
        </thead>
        <tbody>

<?
    for($idx = 1; $idx <= $rows; $idx++) {
        $row = pg_fetch_assoc($result);
        echo "<tr onclick='showBookInfo(".$row["isbn"].");'><th>".$idx."</th>";
        echo "<td>".$row["title"]."</td>";
        echo "<td>".($row["author"] != NULL ? $row["author"] : "(N/A)")."</td>";
        echo "<td>".$row["isbn"]."</td>";
        echo "<td>".$row["price"]."</td></tr>";
    }
?>
        </tbody>
    </table>
    </div><!-- search result -->
    <div class="row">
      <div class="col-md-12 hidden-xs">

        <div class="classic-switch text-center">
          <a href="#" onclick="askBuyBooks();">Can't find the book you want?</a>
        </div>
      </div>
    </div>
<?
    } else if ($succ === 0) {
?>
    <div class="bf-home-search-form txt-center">
    <br>
    <h2>Sorry, no results for your request.</h2>
    <div class="row">
      <div class="col-md-12 hidden-xs">

        <div class="classic-switch text-center">
          <a href="#" onclick="askBuyBooks();">Can't find the book you want?</a>
        </div>
      </div>
    </div>
<?
    } else {
?>
                <br>
<?
    }
?>

            </div>
          </div><!-- /.bf-content-inner-->
        </div><!-- /.bf-content -->
      
      </div><!-- /.bf-content-wrapper -->
    </div>
      <div class="bf-footer-callouts-wrapper">
        <div class="bf-footer-callouts">
          <div class="container-fluid">
            <div class="row">
              <div class="col-md-12 hidden-xs">
                <div class="bf-footer-find-books">
                  <h4>Looking for the books about hacking?</h4>
                  <p>We provide information for books that talks about hacking.<br>Feel free to request information of a book that isn't in our database.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    <div class="bf-footer">
  <!-- Begin phone footer -->
      <div class="container-fluid visible-xs-block">
        <div class="row">
          <div class="col-xs-12">
            <ul class="list-group">
              <li class="list-group-item list-group-control list-group-control-closed"><a href="https://www.bookfinder.com/#link"><span>Search</span></a>
              <div class="list-group-wrapper list-group-closed">
                <ul>
                  <li><a href="https://www.bookfinder.com/">Book Search</a></li>
                  <li><a href="https://www.bookfinder.com/isbn_search/">Search by ISBN</a></li>
                  <li><a href="https://www.bookfinder.com/textbooks/">Textbook Search</a></li>
                  <li><a href="https://www.bookfinder.com/signed_books/">Search Signed Books</a></li>
                  <li><a href="https://www.bookfinder.com/buyback/">Textbook Buyback</a></li>
                </ul>
              </div>
              </li>
              <li class="list-group-item"><a href="https://www.bookfinder.com/help/">Help</a></li>
              <li class="list-group-item"><a href="https://www.bookfinder.com/interact/comments/">Feedback</a></li>
              <li class="list-group-item"><a href="https://www.bookfinder.com/my/preferences/">Preferences</a></li>
            </ul>
          </div>
        </div>
      </div>
    <!-- End phone footer -->
    <!-- Begin default footer -->
    <div class="container-fluid hidden-xs bf-large-footer">
      <div class="bf-large-footer-col bf-large-footer-col1">
        <ul class="list-unstyled bf-large-footer-links">
          <li class="bf-footer-title">Search</li>
          <li><a href="#">Book Search</a></li>
          <li><a href="#">Search by ISBN</a></li>
          <li><a href="#">Search by Author</a></li>
          <li><a href="#">Search by Publication date</a></li>
        </ul>
      </div>
      <div class="bf-large-footer-col bf-large-footer-col2">
        <ul class="list-unstyled bf-large-footer-links">
          <li class="bf-footer-title">Support</li>
          <li><a href="#">Help</a></li>
          <li><a href="#">Feedback</a></li>
          <li><a href="#">Contact Us</a></li>
        </ul>
      </div>
      <div class="bf-large-footer-col bf-large-footer-col3">
        <ul class="list-unstyled bf-large-footer-links">
          <li class="bf-footer-title">About</li>
          <li><a href="">About Us</a></li>
          <li><a href="">Our Booksellers</a></li>
          <li><a href="">For the Press</a></li>
          <li><a href="">Media Mentions</a></li>
        </ul>
      </div>
    </div> 
    <!-- End default footer -->
  </div><!-- /.bf-footer -->
</body>
</html>
