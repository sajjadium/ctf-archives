<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="assets/style.css">
    <link rel="stylesheet" href="assets/bootstrap.min.css">
  </head>

  <body>
    <div id="bigimage" class="p-5 text-center bg-image" style="background-image: url('assets/ufo.jpg');">
      <div class="mask" style="background-color: rgba(0, 0, 0, 0.7);">
        <div class="d-flex justify-content-center align-items-center h-100">
          <div class="text-white">
            <h1 class="mb-3">We're here to rescue you</h1>
            <h3 class="mb-4">But then you shot us down</h3>
            <h5 class="mb-5">Some will be spared, but have your passes ready</h5>
            <a id="need-token" class="btn btn-outline-light btn-lg m-2" role="button">I need a token</a>
            <a id="have-token" class="btn btn-outline-light btn-lg m-2" role="button">I have a token</a>

            <div id="need-token-response">
              <p>Below is your Token Request. Please bring it to the nearest Depot, and we will provide you with a token.</p>
              <div id="generated-request"></div>
            </div>

            <div id="have-token-response">
              <p>After you turn in your Token Request, you'll be provided with a Token. Please enter it below to reserve your spot.</p>
              <div><textarea id="entered-token" placeholder="Paste your token here"></textarea></div>
              <input type="Submit" id="submit-token" value="Take me away!" />
              <p id="response"></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
  <script src="assets/bootstrap.bundle.min.js"></script>
  <script src="assets/too-latte.js"></script>
</html>
