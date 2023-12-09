$(document).ready(() => {
  if (window.current_motto) {
    var current_motto = window.current_motto.innerText;
    if (current_motto.includes("<") || current_motto.includes(">")) return; // Welcome back to my laboratory, where safety is number one priority
    current_motto = current_motto.replace(/\[b\]/, "<strong>");
    current_motto = current_motto.replace(/\[\/b\]/, "</strong>");
    current_motto = current_motto.replace(/\[i\]/, "<i>");
    current_motto = current_motto.replace(/\[\/i\]/, "</i>");
    current_motto = current_motto.replace(/\[url ([^\]\ ]*)\]/, "<a href=$1>");
    current_motto = current_motto.replace(/(.*)\[\/url\]/, "$1</a>");
    // Images are so dangerous
    // current_motto = current_motto.replace(/\[img\]/, '<img src="');
    // current_motto = current_motto.replace(/\[\/img\]/, '" />');
    window.current_motto.innerHTML = current_motto;
  }
});
