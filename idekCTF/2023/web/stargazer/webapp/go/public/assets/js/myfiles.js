let csrf = document.querySelector('meta[name=csrf-token]').content

document.querySelectorAll("ul.myfiles li a").forEach((item) => {
    item.addEventListener("click", (e) => {
        e.preventDefault();
        
        fetch(e.target.href, {
            method: "POST",
            credentials: "include",
            headers: { "X-CSRF-TOKEN": csrf, "Content-Type": "application/x-www-form-urlencoded" },
        })
            .then((res) => res.blob())
            .then((blob) => {
                var file = window.URL.createObjectURL(blob);
                let link = document.createElement("a");
                link.href = file;
                link.download = e.target.href.split("/").pop();
                link.click();
            });
    });
});
