$(document).ready(function () {
  function escapeHtml(text) {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
  
  function escapeHtmlAllowMark(text) {
    return text
      .split(/(<mark>|<\/mark>)/g)
      .map(part => {
        if (part === '<mark>' || part === '</mark>') {
          return part; // Allow <mark> tags, cursed
        }
        return escapeHtml(part);
      })
      .join('');
  }
  
  $("#searchForm").on("submit", function (e) {
    e.preventDefault();
    const query = $("#query").val().trim();
    const language = $("#language").val();
    if (query === "") {
      alert("Please enter a search query.");
      return;
    }
  
    $("#results").empty();
    $("#loading").show();
  
    $.ajax({
      type: "POST",
      url: "/search",
      data: JSON.stringify({ query: query, language: language }),
      contentType: "application/json",
      success: function (response) {
        $("#loading").hide();
        if (response.error) {
          $("#results").html(
            `<div class="alert alert-danger">${escapeHtml(response.error)}</div>`
          );
          return;
        }
  
        if (response.results.length === 0) {
          $("#results").html("<p>No results found.</p>");
          return;
        }
  
        response.results.forEach((result) => {
          const resultItem = `
            <div class="card mb-3">
              <div class="card-body">
                <h5 class="card-title">${escapeHtml(result.fileName)} <span class="badge badge-secondary">${escapeHtml(result.language)}</span></h5>
                <pre><code>${escapeHtmlAllowMark(result.preview)}</code></pre>
                <a href="/view/${encodeURIComponent(result.fileName)}" class="btn btn-primary">View Full Code</a>
              </div>
            </div>
          `;
          $("#results").append(resultItem);
        });
      },
      error: function (xhr) {
        $("#loading").hide();
        $("#results").html(`<div class="alert alert-danger">${escapeHtml(xhr.responseJSON.error) || 'An error occurred.'}</div>`);
      }
    });
  });
});