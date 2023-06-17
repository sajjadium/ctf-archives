<?php
	if(!defined("__MAIN__")) exit("!^_^!");

	include(__TEMPLATE__ . "head.php");
?>
	<style>
    #result: first-child {
      font-weight: bold;
    }

    iframe#calc {
      display: none;
    }
  </style>
  
	<div class="container">
	<iframe src="/api/calculate.php" id="calc"></iframe>

    <div class="row">
      <div class="col">
        <form id="code">
          <div class="form-group">
            <textarea id="textvalue" name="content" class="form-control" placeholder="1+1" rows="10"></textarea>
          </div>
        </form>
        <button class="btn btn-primary" id="calculate" onclick="calculate()">Calculate</button>
        <button class="btn btn-primary" onclick="share()">Share</button>
      </div>
    </div>
  </div>
    <br>
  <main class="container">
      <h2> results: </h2>
        <ul id="results">
        <li></li>
      </ul>
	</main>

  <script>

    window.onload = () => {
      let param = new URLSearchParams(location.search);
      let code = param.get("code");

      if(code) {
        document.getElementById("textvalue").value = atob(code);
      }

      window.onmessage = (e) => {
        if (e.source == window.calc.contentWindow) {
          if(e.data.hacker) {
            location.href = '/';
          }
          document.getElementsByTagName("li")[3].innerText = e.data.result;
        }
      };
    }
    function calculate() {
        let code = document.getElementById("textvalue").value;
        calc.src = "/api/calculate.php#" + btoa(code);
    }
    function share() {
      let code = document.getElementById("textvalue").value;
      alert(`${location.origin + location.pathname}?code=${btoa(code)}`);
    }
</script>
	
<?php
	include(__TEMPLATE__ . "tail.php");
?>