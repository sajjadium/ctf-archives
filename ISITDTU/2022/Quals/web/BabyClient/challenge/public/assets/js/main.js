/* We are watching. */

const $ = document.querySelector.bind(document); // imagine using jQuery

const sanitize = (dirty) => {
    // There is no escape.
    return DOMPurify.sanitize(dirty, { USE_PROFILES: { html: true }, FORBID_ATTR: ["id", "name"] });
};

window.onload = () => {
    // flash messages
    let params = new URLSearchParams(location.search);
    if(location.search.includes("?error=") || location.search.includes("&error=")) {
        $("#flash-error").style.display = "block";
        $("#flash-error").innerHTML = sanitize(params.get("error").slice(0, 300));
    }
    if(location.search.includes("?info=") || location.search.includes("&info=")) {
        $("#flash-info").style.display = "block";
        $("#flash-info").innerHTML = sanitize(params.get("info").slice(0, 300));
    }
    
    // wipe flash
    history.replaceState({}, document.title, location.pathname);
};