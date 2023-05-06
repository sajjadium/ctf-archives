! function(e) {
    "use strict";
    var t;
    t = () => {
        const t = e.querySelector(".dismiss"),
            s = e.querySelector(".sidebar"),
            c = e.querySelector(".overlay"),
            a = e.querySelector(".open-menu");
        s && (t.addEventListener("click", () => {
            s.classList.remove("active"), c.classList.remove("active")
        }), c.addEventListener("click", () => {
            s.classList.remove("active"), c.classList.remove("active")
        }), a.addEventListener("click", e => {
            e.preventDefault(), s.classList.add("active"), c.classList.add("active")
        }), e.querySelector(".nav-link").addEventListener("click", () => {
            s.classList.remove("active"), c.classList.remove("active")
        }))
    }, "loading" != e.readyState ? t() : e.addEventListener("DOMContentLoaded", t)
}(document);

window.onload = () => {
    if(location.search)
        history.replaceState({}, "", location.origin + location.pathname);
};