window.addEventListener('load', function() {
    var params = new URLSearchParams(window.location.search);
    var danger_content = params.get('content') || "!dlrow olleH";
    var content = DOMPurify.sanitize(danger_content);
    document.querySelector('article').innerHTML = content;
});