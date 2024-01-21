$(document).ready(function () {
  function updateStats() {
    $.ajax({
      url: "/api/stats",
      type: "GET",
      success: function (stats) {
        credit = stats["credit"];
        wordsBalance = stats["words_balance"];

        $("#credit").text(credit);
        $("#words_balance").text(wordsBalance);
      },
    });
  }
  updateStats();

  $("#list-public-novels-button").click(function () {
    listNovels("/api/list-public-novels", "public/");
  });

  $("#list-private-novels-button").click(function () {
    listNovels("/api/list-private-novels", "private/");
  });

  $("#charge-form").submit(function (event) {
    event.preventDefault();
    var nwords = $("#nwords").val();
    $.ajax({
      url: "/api/charge?nwords=" + nwords,
      type: "POST",
      success: function (response) {
        if (response.success) {
          $("#charge-result-error").text("");
          $("#charge-result-success").text(response.msg);
          updateStats();
        } else {
          alert(response.msg);
        }
      },
      error: function (error) {
        $("#charge-result-success").text("");
        $("#charge-result-error").text(error.responseJSON.msg);
      },
    });
  });

  function listNovels(url, novelType) {
    $.ajax({
      url: url,
      type: "GET",
      success: function (novels) {
        displayNovels(novels, novelType);
      },
      error: function (error) {
        console.error("Error fetching novels:", error);
      },
    });
  }

  function displayNovels(novels, novelType) {
    $("#novel-list").empty();
    for (var i = 0; i < novels.length; i++) {
      var novelItem = $(
        '<li class="novel-item" style="border: 1px solid #C4141C; padding: 10px;">' +
          novels[i].slice(0,-4).replaceAll('-',' ') +
          ' <button class="read-button" style="color: white; margin-left: 10px"  data-name="' +
          novelType +
          novels[i] +
          '">Read</button></li>'
      );
      $("#novel-list").append(novelItem);
    }
  }

  function displayNovelContent(content) {
    alert(content);
  }

  $("#novel-list").on("click", ".read-button", function () {
    var novelName = $(this).data("name");
    $.ajax({
      url: "/api/read/" + novelName,
      type: "GET",
      success: function (response) {
        if (response.success) {
          displayNovelContent(response.msg);
        } else {
          alert(response.msg);
        }
      },
      error: function (error) {
        alert(error.responseJSON.msg);
      },
    });
  });
});
